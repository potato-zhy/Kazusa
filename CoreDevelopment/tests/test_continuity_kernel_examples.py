from __future__ import annotations

import unittest

from CoreDevelopment.prototypes.continuity_kernel.examples import (
    run_constitutive_canonicalization_scenario,
    run_major_relational_review_scenario,
)


class ContinuityKernelExampleTests(unittest.TestCase):
    def test_major_relational_review_scenario_keeps_mark_open(self) -> None:
        scenario = run_major_relational_review_scenario()

        self.assertEqual(scenario.seed.lineage.state_version, 1)
        self.assertEqual(scenario.ingested.lineage.state_version, 2)
        self.assertEqual(scenario.integrated.lineage.state_version, 3)
        self.assertEqual(len(scenario.ingested.provisional_canonical_marks), 1)
        self.assertEqual(len(scenario.integrated.provisional_canonical_marks), 1)
        self.assertEqual(
            scenario.integrated.audit_log[-1].mark_dispositions,
            {
                scenario.ingested.provisional_canonical_marks[0].mark_id: "carry_forward"
            },
        )
        self.assertFalse(scenario.integrated.audit_log[-1].canonical_impact)
        self.assertIn("provisional_marks: 1", scenario.summary_after_integration)
        self.assertIn("carry_forward", scenario.audit_after_integration)

    def test_constitutive_canonicalization_scenario_promotes_event(self) -> None:
        scenario = run_constitutive_canonicalization_scenario()

        self.assertEqual(scenario.seed.lineage.state_version, 1)
        self.assertEqual(scenario.ingested.lineage.state_version, 3)
        self.assertEqual(scenario.integrated.lineage.state_version, 4)
        self.assertEqual(len(scenario.ingested.provisional_canonical_marks), 1)
        self.assertEqual(scenario.integrated.provisional_canonical_marks, [])
        self.assertEqual(len(scenario.integrated.provisional_signals), 1)
        self.assertEqual(
            scenario.integrated.provisional_signals[0].event_id,
            "event_constitutive_support",
        )
        self.assertEqual(
            scenario.integrated.canonical.autobiographical_signals,
            ["event_constitutive_canonicalization"],
        )
        self.assertTrue(scenario.integrated.audit_log[-1].canonical_impact)
        self.assertIn("canonical_signals: 1", scenario.summary_after_integration)
        self.assertIn("canonicalize", scenario.audit_after_integration)


if __name__ == "__main__":
    unittest.main()
