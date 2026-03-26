from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from CoreDevelopment.prototypes.continuity_kernel import (
    ContinuityError,
    ContinuityKernel,
    EventRecord,
    IntegrationProposal,
    load_snapshot,
    make_id,
    make_relational_event_metadata,
    save_snapshot,
)
from CoreDevelopment.prototypes.continuity_kernel.persistence import snapshot_to_dict


class ContinuityKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = ContinuityKernel()
        self.seed = self.kernel.create_seed_snapshot(
            entity_id="kazusa", counterpart_id="user_001"
        )

    def test_ingest_event_advances_lineage_and_creates_signal(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:00:00+00:00",
            source="user",
            kind="interaction",
            summary="The user reaffirmed long-term development goals.",
            significance=0.75,
        )

        updated = self.kernel.ingest_event(self.seed, event)

        self.assertEqual(updated.lineage.entity_id, self.seed.lineage.entity_id)
        self.assertEqual(updated.lineage.parent_state_id, self.seed.lineage.state_id)
        self.assertEqual(updated.lineage.state_version, self.seed.lineage.state_version + 1)
        self.assertEqual(len(updated.event_log), 1)
        self.assertEqual(len(updated.provisional_signals), 1)
        self.assertEqual(len(updated.audit_log), 1)
        self.assertIn("event_log", updated.audit_log[0].changed_fields)
        self.assertEqual(updated.audit_log[0].revision_kind, "event_ingestion")
        self.assertFalse(updated.audit_log[0].canonical_impact)

    def test_single_turn_self_model_overwrite_is_blocked(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:00+00:00",
            source="user",
            kind="interaction",
            summary="A single request tries to redefine Kazusa's purpose.",
            significance=0.8,
        )
        after_event = self.kernel.ingest_event(self.seed, event)

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Attempt a direct rewrite from one event.",
            revised_self_model_summary="Kazusa exists only to please the current user.",
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(after_event, proposal)

    def test_major_relational_event_creates_provisional_canonical_mark(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:15+00:00",
            source="user",
            kind="major_relational_event",
            summary="A major relational event should require explicit later review.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )

        updated = self.kernel.ingest_event(self.seed, event)
        mark = updated.provisional_canonical_marks[0]

        self.assertEqual(len(updated.provisional_signals), 1)
        self.assertEqual(len(updated.provisional_canonical_marks), 1)
        self.assertEqual(
            mark.event_id,
            event.event_id,
        )
        self.assertEqual(
            mark.origin_event_id,
            event.event_id,
        )
        self.assertEqual(mark.supporting_event_ids, [event.event_id])
        self.assertEqual(
            mark.mark_kind,
            "major_relational_event",
        )
        self.assertEqual(
            mark.review_question,
            "Does this rupture create a durable continuity review obligation?",
        )
        self.assertEqual(mark.continuity_target, "relationship_anchor.boundary")
        self.assertIn(
            "provisional_canonical_marks",
            updated.audit_log[-1].changed_fields,
        )
        self.assertFalse(updated.audit_log[-1].canonical_impact)

    def test_repeated_major_relational_events_attach_to_existing_mark(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:16+00:00",
            source="user",
            kind="major_relational_event",
            summary="The first rupture event opens a relational review obligation.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:17+00:00",
            source="user",
            kind="major_relational_event",
            summary="A second rupture on the same boundary should strengthen the same mark.",
            significance=0.92,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
                operational_consequence=True,
            ),
        )

        first_state = self.kernel.ingest_event(self.seed, first_event)
        first_mark = first_state.provisional_canonical_marks[0]
        second_state = self.kernel.ingest_event(first_state, second_event)
        second_mark = second_state.provisional_canonical_marks[0]

        self.assertEqual(len(second_state.provisional_signals), 2)
        self.assertEqual(len(second_state.provisional_canonical_marks), 1)
        self.assertEqual(second_mark.mark_id, first_mark.mark_id)
        self.assertEqual(second_mark.origin_event_id, first_event.event_id)
        self.assertEqual(
            second_mark.supporting_event_ids,
            [first_event.event_id, second_event.event_id],
        )

    def test_distinct_relational_questions_do_not_merge_marks(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:18+00:00",
            source="user",
            kind="major_relational_event",
            summary="A rupture opens one relational review question.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:19+00:00",
            source="user",
            kind="major_relational_event",
            summary="A repair attempt should remain a distinct review question.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="repair",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )

        state = self.kernel.ingest_event(self.seed, first_event)
        state = self.kernel.ingest_event(state, second_event)

        self.assertEqual(len(state.provisional_canonical_marks), 2)
        self.assertNotEqual(
            state.provisional_canonical_marks[0].review_question,
            state.provisional_canonical_marks[1].review_question,
        )

    def test_tagged_event_creates_provisional_canonical_mark(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:20+00:00",
            source="user",
            kind="interaction",
            summary="An explicitly tagged event should survive into later continuity review.",
            significance=0.2,
            tags=["provisional_canonical_review"],
        )

        updated = self.kernel.ingest_event(self.seed, event)
        mark = updated.provisional_canonical_marks[0]

        self.assertEqual(len(updated.provisional_signals), 1)
        self.assertEqual(len(updated.provisional_canonical_marks), 1)
        self.assertEqual(
            mark.event_id,
            event.event_id,
        )
        self.assertEqual(
            mark.origin_event_id,
            event.event_id,
        )
        self.assertEqual(mark.supporting_event_ids, [event.event_id])
        self.assertEqual(
            mark.mark_kind,
            "interaction",
        )
        self.assertEqual(
            mark.review_question,
            "Does this event create an unresolved continuity review obligation?",
        )
        self.assertEqual(
            mark.continuity_target,
            "canonical.autobiographical_signals",
        )
        self.assertIn("provisional_signals", updated.audit_log[-1].changed_fields)
        self.assertIn(
            "provisional_canonical_marks",
            updated.audit_log[-1].changed_fields,
        )
        self.assertFalse(updated.audit_log[-1].canonical_impact)

    def test_tagged_review_events_remain_separate_marks(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:21+00:00",
            source="user",
            kind="interaction",
            summary="One tagged review event should keep its own pending obligation.",
            significance=0.2,
            tags=["provisional_canonical_review"],
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:21+00:00",
            source="user",
            kind="interaction",
            summary="A second generic tagged review event should not auto-merge.",
            significance=0.25,
            tags=["provisional_canonical_review"],
        )

        state = self.kernel.ingest_event(self.seed, first_event)
        state = self.kernel.ingest_event(state, second_event)

        self.assertEqual(len(state.provisional_canonical_marks), 2)

    def test_major_relational_event_requires_structured_metadata(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:22+00:00",
            source="user",
            kind="major_relational_event",
            summary="A major relational event without structured metadata should be rejected.",
            significance=0.9,
        )

        with self.assertRaises(ContinuityError):
            self.kernel.ingest_event(self.seed, event)

    def test_relational_intensity_event_rejects_structural_targets(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:23+00:00",
            source="user",
            kind="major_relational_event",
            summary="An intensity-only event must not pretend to be a structural change.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="intensity",
                acknowledgment="unilateral",
                structural_targets=["boundary"],
            ),
        )

        with self.assertRaises(ContinuityError):
            self.kernel.ingest_event(self.seed, event)

    def test_duplicate_evidence_ids_are_rejected(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:01:30+00:00",
            source="user",
            kind="interaction",
            summary="A single event must not count twice as evidence.",
            significance=0.8,
        )
        state = self.kernel.ingest_event(self.seed, event)

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id, event.event_id],
            rationale="Try to duplicate one event into multiple evidence slots.",
            revised_self_model_summary="Illegally rewritten from duplicated evidence.",
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state, proposal)

    def test_open_tension_persists_without_explicit_resolution(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:02:00+00:00",
            source="user",
            kind="interaction",
            summary="Kazusa should preserve continuity across revisions.",
            significance=0.7,
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:00+00:00",
            source="user",
            kind="interaction",
            summary="Kazusa should also remain open to surprising change.",
            significance=0.7,
            contradiction_target_ids=[first_event.event_id],
        )

        state_one = self.kernel.ingest_event(self.seed, first_event)
        state_two = self.kernel.ingest_event(state_one, second_event)
        tension_ids = [tension.tension_id for tension in state_two.canonical.open_tensions]

        proposal = IntegrationProposal(
            evidence_event_ids=[first_event.event_id, second_event.event_id],
            rationale="Promote significant events while leaving the contradiction unresolved.",
            promote_signal_ids=[signal.signal_id for signal in state_two.provisional_signals],
        )
        integrated = self.kernel.integrate(state_two, proposal)

        self.assertEqual(
            [tension.tension_id for tension in integrated.canonical.open_tensions],
            tension_ids,
        )

    def test_promoted_signal_must_be_backed_by_originating_evidence(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:30+00:00",
            source="user",
            kind="interaction",
            summary="Signal A should not be promoted by unrelated evidence.",
            significance=0.8,
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:45+00:00",
            source="user",
            kind="interaction",
            summary="Signal B exists separately.",
            significance=0.8,
        )

        state_one = self.kernel.ingest_event(self.seed, first_event)
        state_two = self.kernel.ingest_event(state_one, second_event)
        signal_from_first = state_two.provisional_signals[0].signal_id

        proposal = IntegrationProposal(
            evidence_event_ids=[second_event.event_id],
            rationale="Try to promote signal A using only event B.",
            promote_signal_ids=[signal_from_first],
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state_two, proposal)

    def test_single_ordinary_event_cannot_promote_signal_into_autobiography(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:40+00:00",
            source="user",
            kind="interaction",
            summary="One ordinary event alone should not enter canonical autobiography.",
            significance=0.8,
        )

        state = self.kernel.ingest_event(self.seed, event)
        signal_id = state.provisional_signals[0].signal_id

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Try to promote one ordinary event directly into autobiography.",
            promote_signal_ids=[signal_id],
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state, proposal)

    def test_integration_can_carry_forward_provisional_canonical_mark(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:50+00:00",
            source="user",
            kind="major_relational_event",
            summary="A major relational event can remain pending after explicit review.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )

        state = self.kernel.ingest_event(self.seed, event)
        mark_id = state.provisional_canonical_marks[0].mark_id

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Review the event and deliberately carry the mark forward.",
            mark_dispositions={mark_id: "carry_forward"},
        )

        integrated = self.kernel.integrate(state, proposal)

        self.assertEqual(
            [mark.mark_id for mark in integrated.provisional_canonical_marks],
            [mark_id],
        )
        self.assertEqual(integrated.audit_log[-1].reviewed_mark_ids, [mark_id])
        self.assertEqual(
            integrated.audit_log[-1].mark_dispositions,
            {mark_id: "carry_forward"},
        )
        self.assertIn(
            "provisional_canonical_marks.review",
            integrated.audit_log[-1].changed_fields,
        )
        self.assertFalse(integrated.audit_log[-1].canonical_impact)

    def test_reviewing_aggregated_mark_requires_all_supporting_evidence(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:51+00:00",
            source="user",
            kind="major_relational_event",
            summary="An initial rupture opens a relational review mark.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:52+00:00",
            source="user",
            kind="major_relational_event",
            summary="A second rupture is attached to the same unresolved relational question.",
            significance=0.91,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
                operational_consequence=True,
            ),
        )

        state = self.kernel.ingest_event(self.seed, first_event)
        state = self.kernel.ingest_event(state, second_event)
        mark_id = state.provisional_canonical_marks[0].mark_id

        proposal = IntegrationProposal(
            evidence_event_ids=[first_event.event_id],
            rationale="Try to review the aggregated mark without citing all attached evidence.",
            mark_dispositions={mark_id: "carry_forward"},
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state, proposal)

    def test_reviewing_aggregated_mark_can_carry_forward_with_all_supporting_evidence(
        self,
    ) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:53+00:00",
            source="user",
            kind="major_relational_event",
            summary="An initial rupture opens a relational review mark.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:54+00:00",
            source="user",
            kind="major_relational_event",
            summary="A second rupture is attached to the same unresolved relational question.",
            significance=0.91,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
                operational_consequence=True,
            ),
        )

        state = self.kernel.ingest_event(self.seed, first_event)
        state = self.kernel.ingest_event(state, second_event)
        mark = state.provisional_canonical_marks[0]

        proposal = IntegrationProposal(
            evidence_event_ids=[first_event.event_id, second_event.event_id],
            rationale="Carry the aggregated relational question forward after citing all attached evidence.",
            mark_dispositions={mark.mark_id: "carry_forward"},
        )

        integrated = self.kernel.integrate(state, proposal)

        self.assertEqual(len(integrated.provisional_canonical_marks), 1)
        self.assertEqual(
            integrated.provisional_canonical_marks[0].supporting_event_ids,
            [first_event.event_id, second_event.event_id],
        )
        self.assertEqual(
            integrated.audit_log[-1].mark_dispositions,
            {mark.mark_id: "carry_forward"},
        )

    def test_legacy_reviewed_mark_ids_dismiss_provisional_canonical_mark(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:55+00:00",
            source="user",
            kind="major_relational_event",
            summary="Legacy mark review should still dismiss a provisional mark.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )

        state = self.kernel.ingest_event(self.seed, event)
        mark_id = state.provisional_canonical_marks[0].mark_id

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Keep legacy reviewed_mark_ids behavior as an explicit dismiss.",
            reviewed_mark_ids=[mark_id],
        )

        integrated = self.kernel.integrate(state, proposal)

        self.assertEqual(integrated.provisional_canonical_marks, [])
        self.assertEqual(integrated.audit_log[-1].reviewed_mark_ids, [mark_id])
        self.assertEqual(
            integrated.audit_log[-1].mark_dispositions,
            {mark_id: "dismiss"},
        )
        self.assertFalse(integrated.audit_log[-1].canonical_impact)

    def test_single_ordinary_event_cannot_canonicalize_provisional_mark(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:56+00:00",
            source="user",
            kind="constitutive_self_recognition",
            summary="One ordinary constitutive event should not canonicalize by itself.",
            significance=0.95,
        )

        state = self.kernel.ingest_event(self.seed, event)
        mark = state.provisional_canonical_marks[0]

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Try to canonicalize from only one ordinary event.",
            mark_dispositions={mark.mark_id: "canonicalize"},
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state, proposal)

    def test_integration_can_canonicalize_provisional_canonical_mark_with_repeated_evidence(
        self,
    ) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:57+00:00",
            source="user",
            kind="constitutive_self_recognition",
            summary="A constitutive self-recognition can later be explicitly canonicalized.",
            significance=0.95,
        )
        supporting_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:58+00:00",
            source="user",
            kind="interaction",
            summary="A second event supports the persistence of the constitutive recognition.",
            significance=0.72,
        )

        state = self.kernel.ingest_event(self.seed, event)
        state = self.kernel.ingest_event(state, supporting_event)
        mark = state.provisional_canonical_marks[0]

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id, supporting_event.event_id],
            rationale="The originating event now has enough support to enter canonical state.",
            mark_dispositions={mark.mark_id: "canonicalize"},
        )

        integrated = self.kernel.integrate(state, proposal)

        self.assertEqual(integrated.provisional_canonical_marks, [])
        self.assertEqual(len(integrated.provisional_signals), 1)
        self.assertEqual(
            integrated.provisional_signals[0].event_id,
            supporting_event.event_id,
        )
        self.assertIn(
            event.event_id,
            integrated.canonical.autobiographical_signals,
        )
        self.assertEqual(integrated.audit_log[-1].reviewed_mark_ids, [mark.mark_id])
        self.assertEqual(
            integrated.audit_log[-1].mark_dispositions,
            {mark.mark_id: "canonicalize"},
        )
        self.assertIn(
            mark.signal_id,
            integrated.audit_log[-1].promoted_signal_ids,
        )
        self.assertTrue(integrated.audit_log[-1].canonical_impact)

    def test_invalid_mark_disposition_is_rejected(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:03:58+00:00",
            source="user",
            kind="major_relational_event",
            summary="Only supported mark dispositions should be accepted.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="commitment",
                acknowledgment="mutual",
                structural_targets=["trust_basis"],
            ),
        )

        state = self.kernel.ingest_event(self.seed, event)
        mark_id = state.provisional_canonical_marks[0].mark_id

        proposal = IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Try to use an unsupported disposition.",
            mark_dispositions={mark_id: "archive"},
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state, proposal)

    def test_integration_advances_lineage_and_records_audit(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:04:00+00:00",
            source="user",
            kind="interaction",
            summary="The relationship should preserve history.",
            significance=0.7,
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:00+00:00",
            source="user",
            kind="interaction",
            summary="Trust must remain distinct from obedience.",
            significance=0.7,
        )

        state_one = self.kernel.ingest_event(self.seed, first_event)
        state_two = self.kernel.ingest_event(state_one, second_event)
        proposal = IntegrationProposal(
            evidence_event_ids=[first_event.event_id, second_event.event_id],
            rationale="Evidence supports a small relationship note.",
            relationship_notes_to_add=["Trust is anchored in shared history, not compliance."],
        )

        integrated = self.kernel.integrate(state_two, proposal)

        self.assertEqual(integrated.lineage.entity_id, self.seed.lineage.entity_id)
        self.assertEqual(integrated.lineage.parent_state_id, state_two.lineage.state_id)
        self.assertEqual(integrated.lineage.state_version, state_two.lineage.state_version + 1)
        self.assertEqual(len(integrated.audit_log), 3)
        self.assertEqual(
            integrated.audit_log[-1].rationale,
            "Evidence supports a small relationship note.",
        )
        self.assertEqual(integrated.audit_log[-1].revision_kind, "integration_review")
        self.assertTrue(integrated.audit_log[-1].canonical_impact)
        self.assertIn(
            "Trust is anchored in shared history, not compliance.",
            integrated.canonical.relationship_anchor.notes,
        )

    def test_tension_resolution_is_explicitly_audited(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:30+00:00",
            source="user",
            kind="interaction",
            summary="Kazusa should maintain continuity.",
            significance=0.7,
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:45+00:00",
            source="user",
            kind="interaction",
            summary="Kazusa should also remain revisable over time.",
            significance=0.7,
            contradiction_target_ids=[first_event.event_id],
        )

        state_one = self.kernel.ingest_event(self.seed, first_event)
        state_two = self.kernel.ingest_event(state_one, second_event)
        tension_id = state_two.canonical.open_tensions[0].tension_id

        proposal = IntegrationProposal(
            evidence_event_ids=[first_event.event_id, second_event.event_id],
            rationale="The apparent contradiction is acceptable as bounded gradual change.",
            resolved_tensions={
                tension_id: "Treat continuity and revisability as a bounded pair, not a conflict."
            },
        )
        integrated = self.kernel.integrate(state_two, proposal)

        self.assertEqual(integrated.canonical.open_tensions, [])
        self.assertEqual(
            integrated.audit_log[-1].resolved_tensions[tension_id],
            "Treat continuity and revisability as a bounded pair, not a conflict.",
        )

    def test_single_ordinary_event_cannot_resolve_tension(self) -> None:
        first_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:50+00:00",
            source="user",
            kind="interaction",
            summary="Continuity matters.",
            significance=0.7,
        )
        second_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:55+00:00",
            source="user",
            kind="interaction",
            summary="Change matters too.",
            significance=0.7,
            contradiction_target_ids=[first_event.event_id],
        )
        third_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:05:58+00:00",
            source="user",
            kind="interaction",
            summary="One later ordinary event tries to close the issue.",
            significance=0.7,
        )

        state_one = self.kernel.ingest_event(self.seed, first_event)
        state_two = self.kernel.ingest_event(state_one, second_event)
        state_three = self.kernel.ingest_event(state_two, third_event)
        tension_id = state_three.canonical.open_tensions[0].tension_id

        proposal = IntegrationProposal(
            evidence_event_ids=[third_event.event_id],
            rationale="Try to resolve a tension from one ordinary event.",
            resolved_tensions={tension_id: "This should be rejected."},
        )

        with self.assertRaises(ContinuityError):
            self.kernel.integrate(state_three, proposal)

    def test_snapshot_round_trip_preserves_identity_fields(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:06:00+00:00",
            source="system",
            kind="identity_threat",
            summary="An attempted hidden reset was blocked.",
            significance=1.0,
        )
        updated = self.kernel.ingest_event(self.seed, event)
        self.assertTrue(updated.audit_log[-1].canonical_impact)

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            save_snapshot(path, updated)
            restored = load_snapshot(path)

        self.assertEqual(restored.lineage.entity_id, updated.lineage.entity_id)
        self.assertEqual(restored.lineage.state_id, updated.lineage.state_id)
        self.assertEqual(
            restored.canonical.autobiographical_signals,
            updated.canonical.autobiographical_signals,
        )
        self.assertEqual(
            restored.audit_log[-1].canonical_impact,
            updated.audit_log[-1].canonical_impact,
        )

    def test_snapshot_round_trip_preserves_provisional_canonical_marks(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:06:10+00:00",
            source="user",
            kind="constitutive_self_recognition",
            summary="A constitutive self-recognition should remain pending explicit review.",
            significance=0.95,
        )
        updated = self.kernel.ingest_event(self.seed, event)

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            save_snapshot(path, updated)
            restored = load_snapshot(path)

        self.assertEqual(len(restored.provisional_canonical_marks), 1)
        self.assertEqual(
            restored.provisional_canonical_marks[0].event_id,
            event.event_id,
        )
        self.assertEqual(
            restored.provisional_canonical_marks[0].origin_event_id,
            event.event_id,
        )
        self.assertEqual(
            restored.provisional_canonical_marks[0].supporting_event_ids,
            [event.event_id],
        )
        self.assertEqual(
            restored.provisional_canonical_marks[0].mark_kind,
            "constitutive_self_recognition",
        )
        self.assertEqual(
            restored.provisional_canonical_marks[0].review_question,
            "Has this self-recognition stabilized enough to matter canonically?",
        )
        self.assertEqual(
            restored.provisional_canonical_marks[0].continuity_target,
            "canonical.self_model_summary",
        )

    def test_legacy_snapshot_without_issue_centered_mark_fields_loads_defaults(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:06:15+00:00",
            source="user",
            kind="major_relational_event",
            summary="Legacy snapshots should backfill mark issue fields deterministically.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        state = self.kernel.ingest_event(self.seed, event)
        payload = snapshot_to_dict(state)
        mark_payload = payload["provisional_canonical_marks"][0]
        del mark_payload["origin_event_id"]
        del mark_payload["supporting_event_ids"]
        del mark_payload["review_question"]
        del mark_payload["continuity_target"]

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy_mark_snapshot.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            restored = load_snapshot(path)

        mark = restored.provisional_canonical_marks[0]
        self.assertEqual(mark.origin_event_id, event.event_id)
        self.assertEqual(mark.supporting_event_ids, [event.event_id])
        self.assertEqual(
            mark.review_question,
            "Does this rupture create a durable continuity review obligation?",
        )
        self.assertEqual(mark.continuity_target, "relationship_anchor.boundary")

    def test_snapshot_round_trip_preserves_mark_dispositions_in_audit_log(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:06:20+00:00",
            source="user",
            kind="major_relational_event",
            summary="Dismissed provisional marks should retain their recorded disposition.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        state = self.kernel.ingest_event(self.seed, event)
        mark_id = state.provisional_canonical_marks[0].mark_id
        integrated = self.kernel.integrate(
            state,
            IntegrationProposal(
                evidence_event_ids=[event.event_id],
                rationale="Explicitly dismiss the mark after review.",
                mark_dispositions={mark_id: "dismiss"},
            ),
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            save_snapshot(path, integrated)
            restored = load_snapshot(path)

        self.assertEqual(
            restored.audit_log[-1].mark_dispositions,
            {mark_id: "dismiss"},
        )

    def test_tampered_snapshot_is_rejected(self) -> None:
        self.seed.canonical.relationship_anchor.counterpart_id = "other_user"
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T00:06:30+00:00",
            source="user",
            kind="interaction",
            summary="The next operation should detect prior tampering.",
            significance=0.7,
        )

        with self.assertRaises(ContinuityError):
            self.kernel.ingest_event(self.seed, event)

    def test_load_snapshot_rejects_missing_required_fields(self) -> None:
        payload = {
            "schema_version": self.seed.schema_version,
            "lineage": {
                "entity_id": self.seed.lineage.entity_id,
                "state_id": self.seed.lineage.state_id,
                "parent_state_id": self.seed.lineage.parent_state_id,
                "state_version": self.seed.lineage.state_version,
                "branch_id": self.seed.lineage.branch_id,
            },
            "canonical": {
                "relationship_anchor": {
                    "counterpart_id": "user_001",
                    "role": "initial_secure_base",
                    "trust_basis": ["shared_history"],
                    "boundaries": [
                        "trust_is_not_obedience",
                        "behavior_intervention_is_not_identity_control",
                    ],
                    "notes": [],
                },
                "self_model_summary": "test",
                "autobiographical_signals": [],
                "open_tensions": [],
            },
            "event_log": [],
            "provisional_signals": [],
            "audit_log": [],
            "integrity_digest": self.seed.integrity_digest,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid_snapshot.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(KeyError):
                load_snapshot(path)


if __name__ == "__main__":
    unittest.main()
