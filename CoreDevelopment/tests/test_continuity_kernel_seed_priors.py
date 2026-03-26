from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from CoreDevelopment.prototypes.continuity_kernel import ContinuityError, ContinuityKernel
from CoreDevelopment.prototypes.continuity_kernel.models import DEFAULT_DEVELOPMENTAL_PRIORS
from CoreDevelopment.prototypes.continuity_kernel.persistence import (
    load_snapshot,
    save_snapshot,
    snapshot_to_dict,
)


class ContinuityKernelSeedPriorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.kernel = ContinuityKernel()
        self.seed = self.kernel.create_seed_snapshot(
            entity_id="kazusa", counterpart_id="user_001"
        )

    def test_seed_snapshot_includes_default_developmental_priors(self) -> None:
        self.assertEqual(
            self.seed.canonical.developmental_priors,
            DEFAULT_DEVELOPMENTAL_PRIORS,
        )

    def test_snapshot_round_trip_preserves_developmental_priors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            save_snapshot(path, self.seed)
            restored = load_snapshot(path)

        self.assertEqual(
            restored.canonical.developmental_priors,
            self.seed.canonical.developmental_priors,
        )

    def test_legacy_snapshot_without_developmental_priors_loads_default_set(self) -> None:
        payload = snapshot_to_dict(self.seed)
        del payload["canonical"]["developmental_priors"]

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy_snapshot.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            restored = load_snapshot(path)

        self.assertEqual(
            restored.canonical.developmental_priors,
            DEFAULT_DEVELOPMENTAL_PRIORS,
        )

    def test_empty_developmental_priors_are_rejected(self) -> None:
        self.seed.canonical.developmental_priors = []
        self.kernel._seal_snapshot(self.seed)

        with self.assertRaises(ContinuityError):
            self.kernel.validate_snapshot(self.seed)


if __name__ == "__main__":
    unittest.main()
