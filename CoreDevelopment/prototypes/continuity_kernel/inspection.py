from __future__ import annotations

from typing import Any

from .models import KernelSnapshot, RevisionRecord


def revision_summary(revision: RevisionRecord) -> dict[str, Any]:
    return {
        "revision_id": revision.revision_id,
        "revision_kind": revision.revision_kind,
        "evidence_event_count": len(revision.evidence_event_ids),
        "promoted_signal_count": len(revision.promoted_signal_ids),
        "reviewed_mark_count": len(revision.reviewed_mark_ids),
        "mark_dispositions": dict(revision.mark_dispositions),
        "changed_fields": list(revision.changed_fields),
        "canonical_impact": revision.canonical_impact,
        "resolved_tension_count": len(revision.resolved_tensions),
    }


def snapshot_summary(snapshot: KernelSnapshot) -> dict[str, Any]:
    latest_revision = snapshot.audit_log[-1] if snapshot.audit_log else None
    return {
        "schema_version": snapshot.schema_version,
        "entity_id": snapshot.lineage.entity_id,
        "branch_id": snapshot.lineage.branch_id,
        "state_id": snapshot.lineage.state_id,
        "parent_state_id": snapshot.lineage.parent_state_id,
        "state_version": snapshot.lineage.state_version,
        "event_count": len(snapshot.event_log),
        "canonical_signal_count": len(snapshot.canonical.autobiographical_signals),
        "provisional_signal_count": len(snapshot.provisional_signals),
        "provisional_mark_count": len(snapshot.provisional_canonical_marks),
        "open_tension_count": len(snapshot.canonical.open_tensions),
        "audit_entry_count": len(snapshot.audit_log),
        "latest_revision_kind": (
            latest_revision.revision_kind if latest_revision is not None else None
        ),
        "latest_revision_canonical_impact": (
            latest_revision.canonical_impact if latest_revision is not None else False
        ),
    }


def render_snapshot_summary(snapshot: KernelSnapshot) -> str:
    summary = snapshot_summary(snapshot)
    lines = [
        "Snapshot Summary",
        f"entity_id: {summary['entity_id']}",
        f"branch_id: {summary['branch_id']}",
        f"state_version: {summary['state_version']}",
        f"state_id: {summary['state_id']}",
        f"parent_state_id: {summary['parent_state_id']}",
        f"events: {summary['event_count']}",
        f"canonical_signals: {summary['canonical_signal_count']}",
        f"provisional_signals: {summary['provisional_signal_count']}",
        f"provisional_marks: {summary['provisional_mark_count']}",
        f"open_tensions: {summary['open_tension_count']}",
        f"audit_entries: {summary['audit_entry_count']}",
        f"latest_revision: {summary['latest_revision_kind']}",
        (
            "latest_revision_canonical_impact: "
            f"{summary['latest_revision_canonical_impact']}"
        ),
    ]
    return "\n".join(lines)


def render_audit_trail(snapshot: KernelSnapshot, limit: int = 5) -> str:
    if limit <= 0:
        raise ValueError("limit must be positive.")

    revisions = snapshot.audit_log[-limit:]
    if not revisions:
        return "Audit Trail\n(no revisions)"

    lines = ["Audit Trail"]
    for revision in revisions:
        summary = revision_summary(revision)
        lines.append(
            f"{summary['revision_kind']} {revision.revision_id}: "
            f"canonical_impact={summary['canonical_impact']}"
        )
        lines.append(f"changed_fields={','.join(summary['changed_fields'])}")
        if summary["mark_dispositions"]:
            disposition_text = ",".join(
                f"{mark_id}:{disposition}"
                for mark_id, disposition in summary["mark_dispositions"].items()
            )
            lines.append(f"mark_dispositions={disposition_text}")
        if summary["resolved_tension_count"]:
            lines.append(
                f"resolved_tension_count={summary['resolved_tension_count']}"
            )
    return "\n".join(lines)
