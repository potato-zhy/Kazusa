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
    save_snapshot,
)


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
