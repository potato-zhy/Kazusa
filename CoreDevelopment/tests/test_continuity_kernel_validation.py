from __future__ import annotations

from copy import deepcopy
import unittest

from CoreDevelopment.prototypes.continuity_kernel import (
    ContinuityError,
    ContinuityKernel,
    EventRecord,
    RevisionRecord,
    make_id,
    make_relational_event_metadata,
    utc_now_iso,
)
from CoreDevelopment.prototypes.continuity_kernel.examples import (
    run_constitutive_canonicalization_scenario,
    run_major_relational_review_scenario,
)
from CoreDevelopment.prototypes.continuity_kernel.validation import (
    assert_snapshot_integrity,
    collect_snapshot_issues,
    render_snapshot_validation_report,
)


class ContinuityValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = ContinuityKernel()
        self.seed = self.kernel.create_seed_snapshot(
            entity_id="kazusa", counterpart_id="user_001"
        )

    def test_example_scenarios_pass_snapshot_validation(self) -> None:
        major = run_major_relational_review_scenario()
        constitutive = run_constitutive_canonicalization_scenario()

        for snapshot in (
            major.seed,
            major.ingested,
            major.integrated,
            constitutive.seed,
            constitutive.ingested,
            constitutive.integrated,
        ):
            assert_snapshot_integrity(snapshot)

    def test_validation_rejects_unknown_canonical_event_reference(self) -> None:
        tampered = deepcopy(self.seed)
        tampered.canonical.autobiographical_signals.append("event_missing")
        self.kernel._seal_snapshot(tampered)

        with self.assertRaises(ContinuityError) as context:
            assert_snapshot_integrity(tampered)

        self.assertIn("unknown event_id 'event_missing'", str(context.exception))

    def test_validation_rejects_dangling_mark_signal_reference(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T04:00:00+00:00",
            source="user",
            kind="major_relational_event",
            summary="Validation should catch marks that no longer point at a signal.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        state = self.kernel.ingest_event(self.seed, event)
        tampered = deepcopy(state)
        tampered.provisional_signals = []
        self.kernel._seal_snapshot(tampered)

        issues = collect_snapshot_issues(tampered)
        report = render_snapshot_validation_report(tampered, issues=issues)

        self.assertTrue(
            any("does not exist in provisional_signals" in issue.message for issue in issues)
        )
        self.assertIn("status: invalid", report)

    def test_validation_rejects_mark_without_origin_in_supporting_evidence(self) -> None:
        event = EventRecord(
            event_id=make_id("event"),
            timestamp="2026-03-26T04:00:30+00:00",
            source="user",
            kind="major_relational_event",
            summary="Validation should catch marks whose supporting evidence drops the origin event.",
            significance=0.9,
            metadata=make_relational_event_metadata(
                subtype="rupture",
                acknowledgment="mutual",
                structural_targets=["boundary"],
            ),
        )
        state = self.kernel.ingest_event(self.seed, event)
        tampered = deepcopy(state)
        tampered.provisional_canonical_marks[0].supporting_event_ids = []
        self.kernel._seal_snapshot(tampered)

        with self.assertRaises(ContinuityError) as context:
            assert_snapshot_integrity(tampered)

        self.assertIn("supporting_event_ids", str(context.exception))

    def test_validation_rejects_unknown_audit_evidence_event(self) -> None:
        tampered = deepcopy(self.seed)
        tampered.audit_log.append(
            RevisionRecord(
                revision_id=make_id("revision"),
                timestamp=utc_now_iso(),
                revision_kind="integration_review",
                evidence_event_ids=["event_missing"],
                promoted_signal_ids=[],
                changed_fields=["canonical.relationship_anchor.notes"],
                rationale="Validation should reject dangling audit evidence ids.",
            )
        )
        self.kernel._seal_snapshot(tampered)

        with self.assertRaises(ContinuityError) as context:
            assert_snapshot_integrity(tampered)

        self.assertIn("audit_log[0].evidence_event_ids", str(context.exception))


if __name__ == "__main__":
    unittest.main()
