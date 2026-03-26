from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from CoreDevelopment.prototypes.continuity_kernel.cli import main
from CoreDevelopment.prototypes.continuity_kernel.models import (
    make_relational_event_metadata,
)
from CoreDevelopment.prototypes.continuity_kernel.persistence import load_snapshot


class ContinuityKernelCliTests(unittest.TestCase):
    def test_create_seed_and_summary_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            snapshot_path = temp_path / "seed.json"
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "create-seed",
                        str(snapshot_path),
                        "--entity-id",
                        "kazusa",
                        "--counterpart-id",
                        "user_001",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(snapshot_path.exists())
            self.assertIn("Snapshot Summary", stdout.getvalue())

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["summary", str(snapshot_path)])

            self.assertEqual(exit_code, 0)
            self.assertIn("entity_id: kazusa", stdout.getvalue())

    def test_ingest_event_command_writes_updated_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            seed_path = temp_path / "seed.json"
            event_path = temp_path / "event.json"
            updated_path = temp_path / "updated.json"

            main(["create-seed", str(seed_path)])
            event_path.write_text(
                json.dumps(
                    {
                        "event_id": "event_cli_ingest",
                        "timestamp": "2026-03-26T02:00:00+00:00",
                        "source": "user",
                        "kind": "major_relational_event",
                        "summary": "CLI ingestion should create the same provisional structures.",
                        "significance": 0.9,
                        "metadata": make_relational_event_metadata(
                            subtype="rupture",
                            acknowledgment="mutual",
                            structural_targets=["boundary"],
                        ),
                    }
                ),
                encoding="utf-8",
            )

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "ingest-event",
                        str(seed_path),
                        str(event_path),
                        str(updated_path),
                    ]
                )

            updated = load_snapshot(updated_path)

            self.assertEqual(exit_code, 0)
            self.assertEqual(len(updated.event_log), 1)
            self.assertEqual(len(updated.provisional_signals), 1)
            self.assertEqual(len(updated.provisional_canonical_marks), 1)
            self.assertIn("provisional_marks: 1", stdout.getvalue())

    def test_integrate_and_audit_commands_report_mark_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            seed_path = temp_path / "seed.json"
            first_ingested_path = temp_path / "ingested_first.json"
            ingested_path = temp_path / "ingested.json"
            integrated_path = temp_path / "integrated.json"
            event_path = temp_path / "event.json"
            supporting_event_path = temp_path / "supporting_event.json"
            proposal_path = temp_path / "proposal.json"

            main(["create-seed", str(seed_path)])
            event_path.write_text(
                json.dumps(
                    {
                        "event_id": "event_cli_integrate",
                        "timestamp": "2026-03-26T02:10:00+00:00",
                        "source": "user",
                        "kind": "constitutive_self_recognition",
                        "summary": "CLI integration should canonicalize a reviewed provisional mark.",
                        "significance": 0.95,
                    }
                ),
                encoding="utf-8",
            )
            supporting_event_path.write_text(
                json.dumps(
                    {
                        "event_id": "event_cli_support",
                        "timestamp": "2026-03-26T02:12:00+00:00",
                        "source": "user",
                        "kind": "interaction",
                        "summary": "A second event provides the repeated evidence needed for canonicalization.",
                        "significance": 0.7,
                    }
                ),
                encoding="utf-8",
            )
            main(
                [
                    "ingest-event",
                    str(seed_path),
                    str(event_path),
                    str(first_ingested_path),
                ]
            )
            main(
                [
                    "ingest-event",
                    str(first_ingested_path),
                    str(supporting_event_path),
                    str(ingested_path),
                ]
            )

            ingested = load_snapshot(ingested_path)
            mark_id = ingested.provisional_canonical_marks[0].mark_id
            proposal_path.write_text(
                json.dumps(
                    {
                        "evidence_event_ids": [
                            "event_cli_integrate",
                            "event_cli_support",
                        ],
                        "rationale": "Canonicalize the marked event through the CLI.",
                        "mark_dispositions": {mark_id: "canonicalize"},
                    }
                ),
                encoding="utf-8",
            )

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "integrate",
                        str(ingested_path),
                        str(proposal_path),
                        str(integrated_path),
                    ]
                )

            integrated = load_snapshot(integrated_path)
            self.assertEqual(exit_code, 0)
            self.assertEqual(integrated.provisional_canonical_marks, [])
            self.assertEqual(len(integrated.provisional_signals), 1)
            self.assertEqual(
                integrated.provisional_signals[0].event_id,
                "event_cli_support",
            )
            self.assertIn("canonical_signals: 1", stdout.getvalue())

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["audit", str(integrated_path), "--limit", "1"])

            self.assertEqual(exit_code, 0)
            self.assertIn("integration_review", stdout.getvalue())
            self.assertIn(f"{mark_id}:canonicalize", stdout.getvalue())

    def test_validate_command_reports_ok_for_valid_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            snapshot_path = temp_path / "seed.json"
            stdout = StringIO()

            main(["create-seed", str(snapshot_path)])

            with redirect_stdout(stdout):
                exit_code = main(["validate", str(snapshot_path)])

            self.assertEqual(exit_code, 0)
            self.assertIn("Snapshot Validation", stdout.getvalue())
            self.assertIn("status: ok", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
