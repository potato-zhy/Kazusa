from __future__ import annotations

import unittest

from CoreDevelopment.prototypes.continuity_kernel import (
    ContinuityKernel,
    EventRecord,
    IntegrationProposal,
    make_id,
    make_relational_event_metadata,
)
from CoreDevelopment.prototypes.continuity_kernel.inspection import (
    render_audit_trail,
    render_snapshot_summary,
    revision_summary,
    snapshot_summary,
)


class ContinuityInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = ContinuityKernel()
        self.seed = self.kernel.create_seed_snapshot(
            entity_id="kazusa", counterpart_id="user_001"
        )

    def test_snapshot_summary_reports_counts_after_ingestion(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T01:00:00+00:00",
            source="user",
            kind="major_relational_event",
            summary="A major relational event should remain visible in the snapshot summary.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )

        updated = self.kernel.ingest_event(self.seed, event)
        summary = snapshot_summary(updated)

        self.assertEqual(summary["entity_id"], "kazusa")
        self.assertEqual(summary["state_version"], 2)
        self.assertEqual(summary["event_count"], 1)
        self.assertEqual(summary["provisional_signal_count"], 1)
        self.assertEqual(summary["provisional_mark_count"], 1)
        self.assertEqual(summary["latest_revision_kind"], "event_ingestion")
        self.assertFalse(summary["latest_revision_canonical_impact"])

    def test_render_snapshot_summary_includes_core_state_counts(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T01:01:00+00:00",
            source="user",
            kind="interaction",
            summary="A plain interaction should still show up in the rendered summary.",
            significance=0.75,
        )

        updated = self.kernel.ingest_event(self.seed, event)
        rendered = render_snapshot_summary(updated)

        self.assertIn("Snapshot Summary", rendered)
        self.assertIn("state_version: 2", rendered)
        self.assertIn("events: 1", rendered)
        self.assertIn("provisional_signals: 1", rendered)
        self.assertIn("latest_revision: event_ingestion", rendered)

    def test_render_audit_trail_includes_mark_disposition_details(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T01:02:00+00:00",
            source="user",
            kind="constitutive_self_recognition",
            summary="The audit trail should reveal explicit canonicalization decisions.",
            significance=0.95,
        )
        supporting_event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T01:03:00+00:00",
            source="user",
            kind="interaction",
            summary="A second event should provide the repeated evidence needed for canonicalization.",
            significance=0.72,
        )

        state = self.kernel.ingest_event(self.seed, event)
        state = self.kernel.ingest_event(state, supporting_event)
        mark = state.provisional_canonical_marks[0]
        integrated = self.kernel.integrate(
            state,
            IntegrationProposal(
                evidence_event_ids=[event.event_id, supporting_event.event_id],
                rationale="Canonicalize the marked event after explicit review.",
                mark_dispositions={mark.mark_id: "canonicalize"},
            ),
        )

        revision = revision_summary(integrated.audit_log[-1])
        rendered = render_audit_trail(integrated, limit=2)

        self.assertEqual(revision["mark_dispositions"], {mark.mark_id: "canonicalize"})
        self.assertTrue(revision["canonical_impact"])
        self.assertIn("Audit Trail", rendered)
        self.assertIn("integration_review", rendered)
        self.assertIn("canonical_impact=True", rendered)
        self.assertIn(f"{mark.mark_id}:canonicalize", rendered)


if __name__ == "__main__":
    unittest.main()
