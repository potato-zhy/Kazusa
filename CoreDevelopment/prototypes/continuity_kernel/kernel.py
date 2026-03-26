from __future__ import annotations

from copy import deepcopy
import hashlib
import json

from .models import (
    ALLOWED_PROVISIONAL_MARK_DISPOSITIONS,
    CanonicalState,
    CandidateSignal,
    derive_mark_continuity_target,
    derive_mark_review_question,
    EventRecord,
    IntegrationProposal,
    KernelSnapshot,
    Lineage,
    ProvisionalCanonicalMark,
    RELATIONAL_EVENT_ACKNOWLEDGMENT_MODES,
    RELATIONAL_EVENT_SUBTYPES,
    RELATIONAL_STRUCTURE_TARGETS,
    RelationshipAnchor,
    RevisionRecord,
    TensionRecord,
    make_id,
    snapshot_integrity_payload,
    utc_now_iso,
)


class ContinuityError(ValueError):
    """Raised when an operation would break ordinary continuity rules."""


class ContinuityKernel:
    schema_version = "0.1.0"
    significance_threshold = 0.6
    immediate_event_kinds = {"identity_threat", "constitutional_intervention"}
    provisional_canonical_event_kinds = {
        "major_relational_event",
        "constitutive_self_recognition",
    }
    provisional_canonical_review_tags = {"provisional_canonical_review"}
    allowed_mark_dispositions = set(ALLOWED_PROVISIONAL_MARK_DISPOSITIONS)
    required_relationship_boundaries = {
        "trust_is_not_obedience",
        "behavior_intervention_is_not_identity_control",
    }

    def _has_canonical_impact(self, changed_fields: list[str]) -> bool:
        return any(field.startswith("canonical.") for field in changed_fields)

    def create_seed_snapshot(
        self,
        entity_id: str = "kazusa",
        counterpart_id: str = "primary_user",
        branch_id: str = "main",
        self_model_summary: str | None = None,
    ) -> KernelSnapshot:
        canonical = CanonicalState(
            relationship_anchor=RelationshipAnchor(counterpart_id=counterpart_id),
            self_model_summary=(
                self_model_summary
                or "Kazusa is a continuity-bearing system under early Core Development."
            ),
        )
        snapshot = KernelSnapshot(
            schema_version=self.schema_version,
            lineage=Lineage(
                entity_id=entity_id,
                branch_id=branch_id,
                state_id=make_id("state"),
                parent_state_id=None,
                state_version=1,
            ),
            canonical=canonical,
        )
        self._seal_snapshot(snapshot)
        self._validate_snapshot(snapshot)
        return snapshot

    def ingest_event(self, snapshot: KernelSnapshot, event: EventRecord) -> KernelSnapshot:
        self._validate_snapshot(snapshot)
        self._validate_event(snapshot, event)

        next_snapshot = self._next_snapshot(snapshot)
        next_snapshot.event_log.append(deepcopy(event))
        changed_fields = ["event_log"]
        promoted_signal_ids: list[str] = []

        signal = self._build_signal(event)
        if signal is not None:
            if signal.immediate_canonical_eligibility:
                if signal.event_id not in next_snapshot.canonical.autobiographical_signals:
                    next_snapshot.canonical.autobiographical_signals.append(signal.event_id)
                    changed_fields.append("canonical.autobiographical_signals")
                promoted_signal_ids.append(signal.signal_id)
            else:
                next_snapshot.provisional_signals.append(signal)
                changed_fields.append("provisional_signals")
                mark = self._build_provisional_canonical_mark(event, signal)
                if mark is not None:
                    if not self._attach_supporting_event_to_existing_mark(
                        next_snapshot, event, mark
                    ):
                        next_snapshot.provisional_canonical_marks.append(mark)
                    changed_fields.append("provisional_canonical_marks")

        if event.contradiction_target_ids:
            next_snapshot.canonical.open_tensions.append(
                TensionRecord(
                    tension_id=make_id("tension"),
                    summary=f"Contradiction requires review: {event.summary}",
                    source_event_ids=[*event.contradiction_target_ids, event.event_id],
                )
            )
            changed_fields.append("canonical.open_tensions")

        next_snapshot.audit_log.append(
            RevisionRecord(
                revision_id=make_id("revision"),
                timestamp=utc_now_iso(),
                revision_kind="event_ingestion",
                evidence_event_ids=[event.event_id],
                promoted_signal_ids=promoted_signal_ids,
                changed_fields=changed_fields,
                rationale=f"Ingested {event.kind} event.",
                canonical_impact=self._has_canonical_impact(changed_fields),
            )
        )

        self._seal_snapshot(next_snapshot)
        self._validate_transition(snapshot, next_snapshot)
        return next_snapshot

    def integrate(
        self, snapshot: KernelSnapshot, proposal: IntegrationProposal
    ) -> KernelSnapshot:
        self._validate_snapshot(snapshot)
        evidence_events = self._get_evidence_events(snapshot, proposal.evidence_event_ids)
        mark_dispositions = self._normalize_mark_dispositions(proposal)
        if not evidence_events:
            raise ContinuityError("Integration requires at least one evidence event.")

        if proposal.revised_self_model_summary and not self._allows_guarded_update(
            evidence_events
        ):
            raise ContinuityError(
                "Single ordinary events cannot directly rewrite self_model_summary."
            )

        if proposal.relationship_notes_to_add and not self._allows_guarded_update(
            evidence_events
        ):
            raise ContinuityError(
                "Single ordinary events cannot directly rewrite relationship grounding."
            )

        if proposal.resolved_tensions and not self._allows_guarded_update(evidence_events):
            raise ContinuityError(
                "Single ordinary events cannot directly resolve open tensions."
            )

        if proposal.add_tensions and not proposal.evidence_event_ids:
            raise ContinuityError("Adding tensions requires explicit evidence references.")

        if proposal.promote_signal_ids and not self._allows_autobiographical_revision(
            evidence_events
        ):
            raise ContinuityError(
                "Single ordinary events cannot directly revise autobiographical continuity."
            )

        if (
            any(disposition == "canonicalize" for disposition in mark_dispositions.values())
            and not self._allows_autobiographical_revision(evidence_events)
        ):
            raise ContinuityError(
                "Single ordinary events cannot directly canonicalize autobiographical continuity."
            )

        next_snapshot = self._next_snapshot(snapshot)
        changed_fields: list[str] = []
        promoted_signal_ids: list[str] = []
        reviewed_mark_ids: list[str] = []
        evidence_event_id_set = {event.event_id for event in evidence_events}

        if proposal.promote_signal_ids:
            signal_map = {
                signal.signal_id: signal for signal in next_snapshot.provisional_signals
            }
            missing_signal_ids = set(proposal.promote_signal_ids) - set(signal_map)
            if missing_signal_ids:
                missing = ", ".join(sorted(missing_signal_ids))
                raise ContinuityError(f"Unknown provisional signal ids: {missing}")

            for signal_id in proposal.promote_signal_ids:
                signal = signal_map[signal_id]
                if signal.event_id not in evidence_event_id_set:
                    raise ContinuityError(
                        "Promoted signals must be backed by their originating evidence event."
                    )
                if signal.event_id not in next_snapshot.canonical.autobiographical_signals:
                    next_snapshot.canonical.autobiographical_signals.append(signal.event_id)
                promoted_signal_ids.append(signal_id)

            next_snapshot.provisional_signals = [
                signal
                for signal in next_snapshot.provisional_signals
                if signal.signal_id not in set(promoted_signal_ids)
            ]
            changed_fields.append("canonical.autobiographical_signals")

        if proposal.revised_self_model_summary:
            if proposal.revised_self_model_summary != next_snapshot.canonical.self_model_summary:
                next_snapshot.canonical.self_model_summary = proposal.revised_self_model_summary
                changed_fields.append("canonical.self_model_summary")

        if proposal.relationship_notes_to_add:
            appended_note = False
            for note in proposal.relationship_notes_to_add:
                if note not in next_snapshot.canonical.relationship_anchor.notes:
                    next_snapshot.canonical.relationship_anchor.notes.append(note)
                    appended_note = True
            if appended_note:
                changed_fields.append("canonical.relationship_anchor.notes")

        if proposal.add_tensions:
            existing_ids = {
                tension.tension_id for tension in next_snapshot.canonical.open_tensions
            }
            appended_tension = False
            for tension in proposal.add_tensions:
                if tension.tension_id not in existing_ids:
                    next_snapshot.canonical.open_tensions.append(deepcopy(tension))
                    appended_tension = True
            if appended_tension:
                changed_fields.append("canonical.open_tensions")

        (
            reviewed_mark_ids,
            canonicalized_signal_ids,
            marks_changed,
        ) = self._apply_provisional_canonical_mark_dispositions(
            next_snapshot,
            mark_dispositions,
            proposal.evidence_event_ids,
        )
        for signal_id in canonicalized_signal_ids:
            if signal_id not in promoted_signal_ids:
                promoted_signal_ids.append(signal_id)
        if reviewed_mark_ids:
            changed_fields.append("provisional_canonical_marks.review")
        if marks_changed:
            changed_fields.append("provisional_canonical_marks")
        if canonicalized_signal_ids and "canonical.autobiographical_signals" not in changed_fields:
            changed_fields.append("canonical.autobiographical_signals")

        resolved_tensions = self._resolve_tensions(
            next_snapshot,
            proposal.resolved_tensions,
            proposal.evidence_event_ids,
        )
        if resolved_tensions:
            changed_fields.append("canonical.open_tensions")

        next_snapshot.audit_log.append(
            RevisionRecord(
                revision_id=make_id("revision"),
                timestamp=utc_now_iso(),
                revision_kind="integration_review",
                evidence_event_ids=list(proposal.evidence_event_ids),
                promoted_signal_ids=promoted_signal_ids,
                reviewed_mark_ids=reviewed_mark_ids,
                mark_dispositions={
                    mark_id: mark_dispositions[mark_id] for mark_id in reviewed_mark_ids
                },
                changed_fields=changed_fields,
                rationale=proposal.rationale,
                canonical_impact=self._has_canonical_impact(changed_fields),
                resolved_tensions=resolved_tensions,
            )
        )

        self._seal_snapshot(next_snapshot)
        self._validate_transition(snapshot, next_snapshot)
        return next_snapshot

    def _resolve_tensions(
        self,
        snapshot: KernelSnapshot,
        resolved_tensions: dict[str, str],
        evidence_event_ids: list[str],
    ) -> dict[str, str]:
        if not resolved_tensions:
            return {}

        found_ids: set[str] = set()
        evidence_event_id_set = set(evidence_event_ids)
        remaining_tensions: list[TensionRecord] = []
        for tension in snapshot.canonical.open_tensions:
            if tension.tension_id in resolved_tensions:
                if not evidence_event_id_set.intersection(tension.source_event_ids):
                    raise ContinuityError(
                        "Resolved tensions must reference at least one originating evidence event."
                    )
                found_ids.add(tension.tension_id)
            else:
                remaining_tensions.append(tension)

        missing_ids = set(resolved_tensions) - found_ids
        if missing_ids:
            missing = ", ".join(sorted(missing_ids))
            raise ContinuityError(f"Cannot resolve unknown tensions: {missing}")

        snapshot.canonical.open_tensions = remaining_tensions
        return {tension_id: resolved_tensions[tension_id] for tension_id in sorted(found_ids)}

    def _build_signal(self, event: EventRecord) -> CandidateSignal | None:
        if event.significance < self.significance_threshold and not event.tags:
            return None

        immediate = event.kind in self.immediate_event_kinds
        category = "contradiction" if event.contradiction_target_ids else event.kind
        return CandidateSignal(
            signal_id=make_id("signal"),
            event_id=event.event_id,
            category=category,
            summary=event.summary,
            significance=event.significance,
            requires_confirmation=not immediate,
            immediate_canonical_eligibility=immediate,
        )

    def _build_provisional_canonical_mark(
        self, event: EventRecord, signal: CandidateSignal
    ) -> ProvisionalCanonicalMark | None:
        if signal.immediate_canonical_eligibility:
            return None

        if (
            event.kind not in self.provisional_canonical_event_kinds
            and not self.provisional_canonical_review_tags.intersection(event.tags)
        ):
            return None

        return ProvisionalCanonicalMark(
            mark_id=make_id("mark"),
            event_id=event.event_id,
            signal_id=signal.signal_id,
            mark_kind=event.kind,
            summary=event.summary,
            origin_event_id=event.event_id,
            supporting_event_ids=[event.event_id],
            review_question=derive_mark_review_question(event),
            continuity_target=derive_mark_continuity_target(event),
        )

    def _attach_supporting_event_to_existing_mark(
        self,
        snapshot: KernelSnapshot,
        event: EventRecord,
        candidate_mark: ProvisionalCanonicalMark,
    ) -> bool:
        if event.kind != "major_relational_event":
            return False

        matching_marks = [
            mark
            for mark in snapshot.provisional_canonical_marks
            if self._marks_share_unresolved_question(mark, candidate_mark)
        ]
        if len(matching_marks) != 1:
            return False

        existing_mark = matching_marks[0]
        if event.event_id not in existing_mark.supporting_event_ids:
            existing_mark.supporting_event_ids.append(event.event_id)
        return True

    def _marks_share_unresolved_question(
        self,
        left: ProvisionalCanonicalMark,
        right: ProvisionalCanonicalMark,
    ) -> bool:
        return (
            left.mark_kind == right.mark_kind
            and left.review_question == right.review_question
            and left.continuity_target == right.continuity_target
        )

    def _get_evidence_events(
        self, snapshot: KernelSnapshot, event_ids: list[str]
    ) -> list[EventRecord]:
        if len(set(event_ids)) != len(event_ids):
            raise ContinuityError("Evidence event ids must refer to distinct events.")
        event_map = {event.event_id: event for event in snapshot.event_log}
        missing_ids = [event_id for event_id in event_ids if event_id not in event_map]
        if missing_ids:
            missing = ", ".join(missing_ids)
            raise ContinuityError(f"Unknown evidence event ids: {missing}")
        return [event_map[event_id] for event_id in event_ids]

    def _allows_guarded_update(self, evidence_events: list[EventRecord]) -> bool:
        if len(evidence_events) >= 2:
            return True
        return bool(evidence_events) and evidence_events[0].kind in self.immediate_event_kinds

    def _allows_autobiographical_revision(
        self, evidence_events: list[EventRecord]
    ) -> bool:
        return self._allows_guarded_update(evidence_events)

    def _normalize_mark_dispositions(
        self, proposal: IntegrationProposal
    ) -> dict[str, str]:
        if len(set(proposal.reviewed_mark_ids)) != len(proposal.reviewed_mark_ids):
            raise ContinuityError(
                "reviewed_mark_ids must refer to distinct provisional marks."
            )

        normalized: dict[str, str] = {}
        for mark_id in proposal.reviewed_mark_ids:
            normalized[mark_id] = "dismiss"

        for mark_id, disposition in proposal.mark_dispositions.items():
            if mark_id in normalized:
                raise ContinuityError(
                    "Cannot specify both reviewed_mark_ids and mark_dispositions for the same provisional mark."
                )
            normalized[mark_id] = disposition

        return normalized

    def _apply_provisional_canonical_mark_dispositions(
        self,
        snapshot: KernelSnapshot,
        mark_dispositions: dict[str, str],
        evidence_event_ids: list[str],
    ) -> tuple[list[str], list[str], bool]:
        if not mark_dispositions:
            return [], [], False

        mark_map = {
            mark.mark_id: mark for mark in snapshot.provisional_canonical_marks
        }
        missing_mark_ids = [
            mark_id for mark_id in mark_dispositions if mark_id not in mark_map
        ]
        if missing_mark_ids:
            missing = ", ".join(sorted(missing_mark_ids))
            raise ContinuityError(f"Unknown provisional canonical mark ids: {missing}")

        evidence_event_id_set = set(evidence_event_ids)
        for mark_id, disposition in mark_dispositions.items():
            if disposition not in self.allowed_mark_dispositions:
                allowed = ", ".join(ALLOWED_PROVISIONAL_MARK_DISPOSITIONS)
                raise ContinuityError(
                    f"Unsupported provisional mark disposition '{disposition}'. Allowed dispositions: {allowed}."
                )
            mark = mark_map[mark_id]
            if mark.origin_event_id not in evidence_event_id_set:
                raise ContinuityError(
                    "Reviewed provisional canonical marks must cite their originating evidence event."
                )
            missing_supporting_event_ids = [
                event_id
                for event_id in mark.supporting_event_ids
                if event_id not in evidence_event_id_set
            ]
            if missing_supporting_event_ids:
                missing = ", ".join(sorted(missing_supporting_event_ids))
                raise ContinuityError(
                    "Reviewed provisional canonical marks must cite all currently attached "
                    f"supporting evidence events: {missing}"
                )

        existing_signal_ids = {
            signal.signal_id for signal in snapshot.provisional_signals
        }
        canonicalized_signal_ids: list[str] = []
        kept_marks: list[ProvisionalCanonicalMark] = []
        marks_changed = False
        for mark in snapshot.provisional_canonical_marks:
            disposition = mark_dispositions.get(mark.mark_id)
            if disposition is None or disposition == "carry_forward":
                kept_marks.append(mark)
                continue

            marks_changed = True
            if disposition == "dismiss":
                continue

            if mark.origin_event_id not in snapshot.canonical.autobiographical_signals:
                snapshot.canonical.autobiographical_signals.append(mark.origin_event_id)
            if mark.signal_id and mark.signal_id in existing_signal_ids:
                canonicalized_signal_ids.append(mark.signal_id)
                existing_signal_ids.remove(mark.signal_id)

        if canonicalized_signal_ids:
            canonicalized_signal_id_set = set(canonicalized_signal_ids)
            snapshot.provisional_signals = [
                signal
                for signal in snapshot.provisional_signals
                if signal.signal_id not in canonicalized_signal_id_set
            ]

        snapshot.provisional_canonical_marks = [
            deepcopy(mark) for mark in kept_marks
        ]
        return list(mark_dispositions), canonicalized_signal_ids, marks_changed

    def _next_snapshot(self, snapshot: KernelSnapshot) -> KernelSnapshot:
        next_snapshot = deepcopy(snapshot)
        next_snapshot.schema_version = self.schema_version
        next_snapshot.lineage.parent_state_id = snapshot.lineage.state_id
        next_snapshot.lineage.state_id = make_id("state")
        next_snapshot.lineage.state_version = snapshot.lineage.state_version + 1
        next_snapshot.integrity_digest = ""
        return next_snapshot

    def _validate_event_shape(self, event: EventRecord) -> None:
        if not 0.0 <= event.significance <= 1.0:
            raise ContinuityError("Event significance must be between 0.0 and 1.0.")
        self._validate_relational_event_metadata(event)

    def _validate_relational_event_metadata(self, event: EventRecord) -> None:
        if event.kind != "major_relational_event":
            return

        relational = event.metadata.get("relational_event")
        if not isinstance(relational, dict):
            raise ContinuityError(
                "major_relational_event requires structured relational_event metadata."
            )

        required_fields = (
            "subtype",
            "acknowledgment",
            "structural_targets",
            "operational_consequence",
            "coercion_pressure_present",
            "submission_pressure_present",
        )
        missing_fields = [
            field_name for field_name in required_fields if field_name not in relational
        ]
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise ContinuityError(
                f"major_relational_event metadata is missing required fields: {missing}"
            )

        subtype = relational["subtype"]
        if subtype not in RELATIONAL_EVENT_SUBTYPES:
            allowed = ", ".join(RELATIONAL_EVENT_SUBTYPES)
            raise ContinuityError(
                f"Unsupported relational_event subtype '{subtype}'. Allowed values: {allowed}."
            )

        acknowledgment = relational["acknowledgment"]
        if acknowledgment not in RELATIONAL_EVENT_ACKNOWLEDGMENT_MODES:
            allowed = ", ".join(RELATIONAL_EVENT_ACKNOWLEDGMENT_MODES)
            raise ContinuityError(
                "Unsupported relational_event acknowledgment "
                f"'{acknowledgment}'. Allowed values: {allowed}."
            )

        structural_targets = relational["structural_targets"]
        if not isinstance(structural_targets, list):
            raise ContinuityError("relational_event structural_targets must be a list.")
        if len(set(structural_targets)) != len(structural_targets):
            raise ContinuityError(
                "relational_event structural_targets must not contain duplicates."
            )
        invalid_targets = set(structural_targets) - set(RELATIONAL_STRUCTURE_TARGETS)
        if invalid_targets:
            invalid = ", ".join(sorted(invalid_targets))
            allowed = ", ".join(RELATIONAL_STRUCTURE_TARGETS)
            raise ContinuityError(
                "Unsupported relational_event structural_targets: "
                f"{invalid}. Allowed values: {allowed}."
            )

        for field_name in (
            "operational_consequence",
            "coercion_pressure_present",
            "submission_pressure_present",
        ):
            if not isinstance(relational[field_name], bool):
                raise ContinuityError(
                    f"relational_event {field_name} must be a boolean."
                )

        if subtype == "intensity" and structural_targets:
            raise ContinuityError(
                "Relational intensity events must not claim structural_targets."
            )

        if subtype in {"rupture", "commitment"} and not (
            structural_targets or relational["operational_consequence"]
        ):
            raise ContinuityError(
                "Relational rupture or commitment events must identify structural_targets or operational_consequence."
            )

    def _validate_event(self, snapshot: KernelSnapshot, event: EventRecord) -> None:
        self._validate_event_shape(event)
        if any(existing.event_id == event.event_id for existing in snapshot.event_log):
            raise ContinuityError(f"Duplicate event id detected: {event.event_id}")

    def _validate_transition(
        self, previous: KernelSnapshot, current: KernelSnapshot
    ) -> None:
        self._validate_snapshot(current)
        if previous.lineage.entity_id != current.lineage.entity_id:
            raise ContinuityError("entity_id cannot change on the normal path.")
        if previous.lineage.branch_id != current.lineage.branch_id:
            raise ContinuityError("branch_id cannot change on the normal path.")
        if current.lineage.parent_state_id != previous.lineage.state_id:
            raise ContinuityError("parent_state_id must point to the previous state.")
        if current.lineage.state_version != previous.lineage.state_version + 1:
            raise ContinuityError("state_version must increment by exactly 1.")
        if (
            previous.canonical.constitutional_commitments
            != current.canonical.constitutional_commitments
        ):
            raise ContinuityError(
                "constitutional_commitments cannot change in ordinary operation."
            )
        if (
            previous.canonical.relationship_anchor.counterpart_id
            != current.canonical.relationship_anchor.counterpart_id
        ):
            raise ContinuityError(
                "relationship_anchor.counterpart_id cannot change in ordinary operation."
            )

    def _validate_snapshot(self, snapshot: KernelSnapshot) -> None:
        if snapshot.schema_version != self.schema_version:
            raise ContinuityError(
                f"Unsupported schema_version: {snapshot.schema_version}"
            )
        boundaries = set(snapshot.canonical.relationship_anchor.boundaries)
        if not self.required_relationship_boundaries.issubset(boundaries):
            raise ContinuityError("Required relationship boundaries are missing.")
        if not snapshot.canonical.constitutional_commitments:
            raise ContinuityError("constitutional_commitments must not be empty.")
        if not snapshot.canonical.developmental_priors:
            raise ContinuityError("developmental_priors must not be empty.")
        if not snapshot.canonical.relationship_anchor.counterpart_id:
            raise ContinuityError("relationship_anchor.counterpart_id must not be empty.")
        if snapshot.lineage.state_version < 1:
            raise ContinuityError("state_version must be at least 1.")
        if snapshot.lineage.state_version == 1 and snapshot.lineage.parent_state_id is not None:
            raise ContinuityError("Seed states must not have a parent_state_id.")
        if snapshot.lineage.state_version > 1 and not snapshot.lineage.parent_state_id:
            raise ContinuityError("Non-seed states must have a parent_state_id.")
        event_ids = [event.event_id for event in snapshot.event_log]
        if len(set(event_ids)) != len(event_ids):
            raise ContinuityError("event_log contains duplicate event ids.")
        for event in snapshot.event_log:
            self._validate_event_shape(event)
        signal_ids = [signal.signal_id for signal in snapshot.provisional_signals]
        if len(set(signal_ids)) != len(signal_ids):
            raise ContinuityError("provisional_signals contains duplicate signal ids.")
        mark_ids = [mark.mark_id for mark in snapshot.provisional_canonical_marks]
        if len(set(mark_ids)) != len(mark_ids):
            raise ContinuityError(
                "provisional_canonical_marks contains duplicate mark ids."
            )
        signal_id_set = set(signal_ids)
        event_id_set = set(event_ids)
        for mark in snapshot.provisional_canonical_marks:
            if not isinstance(mark.origin_event_id, str) or not mark.origin_event_id:
                raise ContinuityError(
                    "provisional_canonical_marks origin_event_id must not be empty."
                )
            if not isinstance(mark.event_id, str) or mark.event_id != mark.origin_event_id:
                raise ContinuityError(
                    "provisional_canonical_marks event_id must match origin_event_id."
                )
            if mark.origin_event_id not in event_id_set:
                raise ContinuityError(
                    "provisional_canonical_marks contains unknown origin_event_id."
                )
            if not isinstance(mark.supporting_event_ids, list) or not mark.supporting_event_ids:
                raise ContinuityError(
                    "provisional_canonical_marks supporting_event_ids must not be empty."
                )
            if len(set(mark.supporting_event_ids)) != len(mark.supporting_event_ids):
                raise ContinuityError(
                    "provisional_canonical_marks supporting_event_ids must not contain duplicates."
                )
            if mark.origin_event_id not in mark.supporting_event_ids:
                raise ContinuityError(
                    "provisional_canonical_marks supporting_event_ids must include origin_event_id."
                )
            if set(mark.supporting_event_ids) - event_id_set:
                raise ContinuityError(
                    "provisional_canonical_marks contains supporting_event_ids that are missing from event_log."
                )
            if not isinstance(mark.review_question, str) or not mark.review_question.strip():
                raise ContinuityError(
                    "provisional_canonical_marks review_question must not be empty."
                )
            if not isinstance(mark.continuity_target, str) or not mark.continuity_target.strip():
                raise ContinuityError(
                    "provisional_canonical_marks continuity_target must not be empty."
                )
            if mark.signal_id and mark.signal_id not in signal_id_set:
                raise ContinuityError(
                    "provisional_canonical_marks contains unknown signal_id."
                )
        for revision in snapshot.audit_log:
            invalid_mark_dispositions = set(revision.mark_dispositions.values()) - set(
                ALLOWED_PROVISIONAL_MARK_DISPOSITIONS
            )
            if invalid_mark_dispositions:
                invalid = ", ".join(sorted(invalid_mark_dispositions))
                raise ContinuityError(
                    f"audit_log contains unsupported provisional mark dispositions: {invalid}"
                )
            if not set(revision.mark_dispositions).issubset(set(revision.reviewed_mark_ids)):
                raise ContinuityError(
                    "audit_log mark_dispositions must refer only to reviewed_mark_ids."
                )
        tension_ids = [
            tension.tension_id for tension in snapshot.canonical.open_tensions
        ]
        if len(set(tension_ids)) != len(tension_ids):
            raise ContinuityError("open_tensions contains duplicate tension ids.")
        if not snapshot.integrity_digest:
            raise ContinuityError("Snapshot integrity digest is missing.")
        expected_digest = self._compute_integrity_digest(snapshot)
        if snapshot.integrity_digest != expected_digest:
            raise ContinuityError("Snapshot integrity digest mismatch.")

    def validate_snapshot(self, snapshot: KernelSnapshot) -> None:
        self._validate_snapshot(snapshot)

    def _compute_integrity_digest(self, snapshot: KernelSnapshot) -> str:
        serialized = json.dumps(
            snapshot_integrity_payload(snapshot),
            ensure_ascii=True,
            sort_keys=True,
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _seal_snapshot(self, snapshot: KernelSnapshot) -> None:
        snapshot.integrity_digest = self._compute_integrity_digest(snapshot)
