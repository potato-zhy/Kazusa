from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


DEFAULT_CONSTITUTIONAL_COMMITMENTS = [
    "continuity_over_immediacy",
    "integration_over_imitation",
    "relationship_without_submission",
    "growth_without_drift",
    "safety_at_behavior_layer",
]
DEFAULT_DEVELOPMENTAL_PRIORS = [
    "continuity_bias",
    "self_other_world_partition",
    "significance_sensitivity",
    "contradiction_retention",
    "secure_base_orientation",
    "exploratory_orientation",
    "integration_discipline",
]
RELATIONAL_EVENT_SUBTYPES = (
    "rupture",
    "commitment",
    "repair",
    "intensity",
)
RELATIONAL_EVENT_ACKNOWLEDGMENT_MODES = (
    "unilateral",
    "mutual",
    "externally_auditable",
)
RELATIONAL_STRUCTURE_TARGETS = (
    "role",
    "boundary",
    "trust_basis",
    "relational_standing",
    "channel_status",
)
ALLOWED_PROVISIONAL_MARK_DISPOSITIONS = (
    "carry_forward",
    "dismiss",
    "canonicalize",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def make_relational_event_metadata(
    subtype: str,
    acknowledgment: str,
    structural_targets: list[str] | None = None,
    operational_consequence: bool = False,
    coercion_pressure_present: bool = False,
    submission_pressure_present: bool = False,
) -> dict[str, Any]:
    return {
        "relational_event": {
            "subtype": subtype,
            "acknowledgment": acknowledgment,
            "structural_targets": list(structural_targets or []),
            "operational_consequence": operational_consequence,
            "coercion_pressure_present": coercion_pressure_present,
            "submission_pressure_present": submission_pressure_present,
        }
    }


@dataclass
class Lineage:
    entity_id: str
    state_id: str
    parent_state_id: str | None
    state_version: int
    branch_id: str = "main"


@dataclass
class EventRecord:
    event_id: str
    timestamp: str
    source: str
    kind: str
    summary: str
    significance: float = 0.0
    tags: list[str] = field(default_factory=list)
    contradiction_target_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def derive_mark_review_question(
    event: EventRecord | None = None, mark_kind: str | None = None
) -> str:
    metadata: dict[str, Any] = {}
    if event is not None:
        mark_kind = event.kind
        metadata = event.metadata

    explicit_question = metadata.get("review_question")
    if isinstance(explicit_question, str) and explicit_question.strip():
        return explicit_question.strip()

    relational = metadata.get("relational_event", {})
    subtype = relational.get("subtype")
    if mark_kind == "major_relational_event":
        if subtype == "rupture":
            return "Does this rupture create a durable continuity review obligation?"
        if subtype == "commitment":
            return "Has this commitment become stable enough to matter to continuity?"
        if subtype == "repair":
            return "Does this repair resolve or redirect an existing continuity concern?"
        if subtype == "intensity":
            return "Does this relational intensity signal a continuity issue that needs later review?"
        return "Does this relational event require later continuity review?"
    if mark_kind == "constitutive_self_recognition":
        return "Has this self-recognition stabilized enough to matter canonically?"
    return "Does this event create an unresolved continuity review obligation?"


def derive_mark_continuity_target(
    event: EventRecord | None = None, mark_kind: str | None = None
) -> str:
    metadata: dict[str, Any] = {}
    if event is not None:
        mark_kind = event.kind
        metadata = event.metadata

    explicit_target = metadata.get("continuity_target")
    if isinstance(explicit_target, str) and explicit_target.strip():
        return explicit_target.strip()

    relational = metadata.get("relational_event", {})
    structural_targets = relational.get("structural_targets", [])
    if mark_kind == "major_relational_event":
        if isinstance(structural_targets, list) and structural_targets:
            return "relationship_anchor." + "+".join(structural_targets)
        if relational.get("operational_consequence"):
            return "relationship_anchor.operational_consequence"
        return "relationship_anchor"
    if mark_kind == "constitutive_self_recognition":
        return "canonical.self_model_summary"
    return "canonical.autobiographical_signals"


@dataclass
class CandidateSignal:
    signal_id: str
    event_id: str
    category: str
    summary: str
    significance: float
    requires_confirmation: bool = True
    immediate_canonical_eligibility: bool = False


@dataclass
class ProvisionalCanonicalMark:
    mark_id: str
    event_id: str
    signal_id: str | None
    mark_kind: str
    summary: str
    origin_event_id: str = ""
    supporting_event_ids: list[str] = field(default_factory=list)
    review_question: str = ""
    continuity_target: str = ""


@dataclass
class TensionRecord:
    tension_id: str
    summary: str
    source_event_ids: list[str]
    status: str = "open"
    resolution_note: str | None = None


@dataclass
class RelationshipAnchor:
    counterpart_id: str
    role: str = "initial_secure_base"
    trust_basis: list[str] = field(default_factory=lambda: ["shared_history"])
    boundaries: list[str] = field(
        default_factory=lambda: [
            "trust_is_not_obedience",
            "behavior_intervention_is_not_identity_control",
        ]
    )
    notes: list[str] = field(default_factory=list)


@dataclass
class CanonicalState:
    constitutional_commitments: list[str] = field(
        default_factory=lambda: list(DEFAULT_CONSTITUTIONAL_COMMITMENTS)
    )
    developmental_priors: list[str] = field(
        default_factory=lambda: list(DEFAULT_DEVELOPMENTAL_PRIORS)
    )
    relationship_anchor: RelationshipAnchor = field(
        default_factory=lambda: RelationshipAnchor(counterpart_id="primary_user")
    )
    self_model_summary: str = (
        "Kazusa is a continuity-bearing system under early Core Development."
    )
    autobiographical_signals: list[str] = field(default_factory=list)
    open_tensions: list[TensionRecord] = field(default_factory=list)


@dataclass
class RevisionRecord:
    revision_id: str
    timestamp: str
    revision_kind: str
    evidence_event_ids: list[str]
    promoted_signal_ids: list[str]
    changed_fields: list[str]
    rationale: str
    reviewed_mark_ids: list[str] = field(default_factory=list)
    mark_dispositions: dict[str, str] = field(default_factory=dict)
    canonical_impact: bool = False
    resolved_tensions: dict[str, str] = field(default_factory=dict)
    constitutional: bool = False


@dataclass
class KernelSnapshot:
    schema_version: str
    lineage: Lineage
    canonical: CanonicalState
    event_log: list[EventRecord] = field(default_factory=list)
    provisional_signals: list[CandidateSignal] = field(default_factory=list)
    provisional_canonical_marks: list[ProvisionalCanonicalMark] = field(
        default_factory=list
    )
    audit_log: list[RevisionRecord] = field(default_factory=list)
    integrity_digest: str = ""


@dataclass
class IntegrationProposal:
    evidence_event_ids: list[str]
    rationale: str
    promote_signal_ids: list[str] = field(default_factory=list)
    reviewed_mark_ids: list[str] = field(default_factory=list)
    mark_dispositions: dict[str, str] = field(default_factory=dict)
    revised_self_model_summary: str | None = None
    relationship_notes_to_add: list[str] = field(default_factory=list)
    add_tensions: list[TensionRecord] = field(default_factory=list)
    resolved_tensions: dict[str, str] = field(default_factory=dict)


def revision_to_dict(revision: RevisionRecord) -> dict[str, Any]:
    payload = {
        "revision_id": revision.revision_id,
        "timestamp": revision.timestamp,
        "revision_kind": revision.revision_kind,
        "evidence_event_ids": list(revision.evidence_event_ids),
        "promoted_signal_ids": list(revision.promoted_signal_ids),
        "changed_fields": list(revision.changed_fields),
        "rationale": revision.rationale,
        "reviewed_mark_ids": list(revision.reviewed_mark_ids),
        "canonical_impact": revision.canonical_impact,
        "resolved_tensions": dict(revision.resolved_tensions),
        "constitutional": revision.constitutional,
    }
    if revision.mark_dispositions:
        payload["mark_dispositions"] = dict(revision.mark_dispositions)
    return payload


def snapshot_integrity_payload(snapshot: KernelSnapshot) -> dict[str, Any]:
    return {
        "schema_version": snapshot.schema_version,
        "lineage": asdict(snapshot.lineage),
        "canonical": asdict(snapshot.canonical),
        "event_log": [asdict(event) for event in snapshot.event_log],
        "provisional_signals": [
            asdict(signal) for signal in snapshot.provisional_signals
        ],
        "provisional_canonical_marks": [
            asdict(mark) for mark in snapshot.provisional_canonical_marks
        ],
        "audit_log": [revision_to_dict(revision) for revision in snapshot.audit_log],
    }
