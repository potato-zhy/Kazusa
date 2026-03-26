from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import (
    CanonicalState,
    CandidateSignal,
    EventRecord,
    KernelSnapshot,
    Lineage,
    ProvisionalCanonicalMark,
    RelationshipAnchor,
    RevisionRecord,
    TensionRecord,
)


def snapshot_to_dict(snapshot: KernelSnapshot) -> dict:
    return asdict(snapshot)


def snapshot_from_dict(payload: dict) -> KernelSnapshot:
    canonical_payload = payload["canonical"]
    relationship_anchor = RelationshipAnchor(**canonical_payload["relationship_anchor"])
    open_tensions = [
        TensionRecord(**tension_payload)
        for tension_payload in canonical_payload["open_tensions"]
    ]
    canonical = CanonicalState(
        constitutional_commitments=canonical_payload["constitutional_commitments"],
        relationship_anchor=relationship_anchor,
        self_model_summary=canonical_payload["self_model_summary"],
        autobiographical_signals=canonical_payload["autobiographical_signals"],
        open_tensions=open_tensions,
    )

    event_log = [EventRecord(**event_payload) for event_payload in payload["event_log"]]
    provisional_signals = [
        CandidateSignal(**signal_payload)
        for signal_payload in payload["provisional_signals"]
    ]
    provisional_canonical_marks = [
        ProvisionalCanonicalMark(**mark_payload)
        for mark_payload in payload.get("provisional_canonical_marks", [])
    ]
    audit_log = [
        RevisionRecord(
            revision_id=revision_payload["revision_id"],
            timestamp=revision_payload["timestamp"],
            revision_kind=revision_payload.get("revision_kind", "integration_review"),
            evidence_event_ids=revision_payload["evidence_event_ids"],
            promoted_signal_ids=revision_payload["promoted_signal_ids"],
            reviewed_mark_ids=revision_payload.get("reviewed_mark_ids", []),
            changed_fields=revision_payload["changed_fields"],
            rationale=revision_payload["rationale"],
            canonical_impact=revision_payload.get("canonical_impact", False),
            resolved_tensions=revision_payload.get("resolved_tensions", {}),
            constitutional=revision_payload.get("constitutional", False),
        )
        for revision_payload in payload["audit_log"]
    ]

    return KernelSnapshot(
        schema_version=payload["schema_version"],
        lineage=Lineage(**payload["lineage"]),
        canonical=canonical,
        event_log=event_log,
        provisional_signals=provisional_signals,
        provisional_canonical_marks=provisional_canonical_marks,
        audit_log=audit_log,
        integrity_digest=payload["integrity_digest"],
    )


def save_snapshot(path: str | Path, snapshot: KernelSnapshot) -> None:
    from .kernel import ContinuityKernel

    ContinuityKernel().validate_snapshot(snapshot)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(snapshot_to_dict(snapshot), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def load_snapshot(path: str | Path) -> KernelSnapshot:
    from .kernel import ContinuityKernel

    target = Path(path)
    snapshot = snapshot_from_dict(json.loads(target.read_text(encoding="utf-8")))
    ContinuityKernel().validate_snapshot(snapshot)
    return snapshot
