from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .kernel import ContinuityError, ContinuityKernel
from .models import KernelSnapshot


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def collect_snapshot_issues(snapshot: KernelSnapshot) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    try:
        ContinuityKernel().validate_snapshot(snapshot)
    except ContinuityError as exc:
        issues.append(ValidationIssue(path="snapshot", message=str(exc)))

    event_ids = [event.event_id for event in snapshot.event_log]
    event_id_set = set(event_ids)

    for event_id in _duplicates(snapshot.canonical.autobiographical_signals):
        issues.append(
            ValidationIssue(
                path="canonical.autobiographical_signals",
                message=f"duplicate canonical event_id '{event_id}' detected.",
            )
        )

    for event_id in snapshot.canonical.autobiographical_signals:
        if event_id not in event_id_set:
            issues.append(
                ValidationIssue(
                    path="canonical.autobiographical_signals",
                    message=f"unknown event_id '{event_id}'.",
                )
            )

    signal_ids = [signal.signal_id for signal in snapshot.provisional_signals]
    signal_id_set = set(signal_ids)
    for index, signal in enumerate(snapshot.provisional_signals):
        if signal.event_id not in event_id_set:
            issues.append(
                ValidationIssue(
                    path=f"provisional_signals[{index}]",
                    message=(
                        f"event_id '{signal.event_id}' does not exist in event_log."
                    ),
                )
            )

    mark_event_ids: set[str] = set()
    for index, mark in enumerate(snapshot.provisional_canonical_marks):
        mark_event_ids.add(mark.origin_event_id)
        if mark.event_id not in event_id_set:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message=f"event_id '{mark.event_id}' does not exist in event_log.",
                )
            )
        if not isinstance(mark.origin_event_id, str) or not mark.origin_event_id:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message="origin_event_id must not be empty.",
                )
            )
        elif mark.origin_event_id not in event_id_set:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message=(
                        f"origin_event_id '{mark.origin_event_id}' does not exist in event_log."
                    ),
                )
            )
        if mark.event_id != mark.origin_event_id:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message="event_id must match origin_event_id.",
                )
            )
        if not isinstance(mark.supporting_event_ids, list) or not mark.supporting_event_ids:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message="supporting_event_ids must not be empty.",
                )
            )
        supporting_event_ids = (
            mark.supporting_event_ids if isinstance(mark.supporting_event_ids, list) else []
        )
        for event_id in _duplicates(supporting_event_ids):
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}].supporting_event_ids",
                    message=f"duplicate supporting event_id '{event_id}' detected.",
                )
            )
        if mark.origin_event_id and mark.origin_event_id not in supporting_event_ids:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}].supporting_event_ids",
                    message="origin_event_id must be included in supporting_event_ids.",
                )
            )
        for event_id in supporting_event_ids:
            if event_id not in event_id_set:
                issues.append(
                    ValidationIssue(
                        path=f"provisional_canonical_marks[{index}].supporting_event_ids",
                        message=f"unknown event_id '{event_id}'.",
                    )
                )
        if not isinstance(mark.review_question, str) or not mark.review_question.strip():
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message="review_question must not be empty.",
                )
            )
        if not isinstance(mark.continuity_target, str) or not mark.continuity_target.strip():
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message="continuity_target must not be empty.",
                )
            )
        if mark.signal_id and mark.signal_id not in signal_id_set:
            issues.append(
                ValidationIssue(
                    path=f"provisional_canonical_marks[{index}]",
                    message=(
                        f"signal_id '{mark.signal_id}' does not exist in provisional_signals."
                    ),
                )
            )

    for event_id in sorted(mark_event_ids.intersection(event_id_set)):
        if event_id in snapshot.canonical.autobiographical_signals:
            issues.append(
                ValidationIssue(
                    path="provisional_canonical_marks",
                    message=(
                        f"event_id '{event_id}' cannot be both provisional and canonical."
                    ),
                )
            )

    revision_ids = [revision.revision_id for revision in snapshot.audit_log]
    for revision_id in _duplicates(revision_ids):
        issues.append(
            ValidationIssue(
                path="audit_log",
                message=f"duplicate revision_id '{revision_id}' detected.",
            )
        )

    for index, revision in enumerate(snapshot.audit_log):
        for event_id in _duplicates(revision.evidence_event_ids):
            issues.append(
                ValidationIssue(
                    path=f"audit_log[{index}].evidence_event_ids",
                    message=f"duplicate evidence event_id '{event_id}' detected.",
                )
            )
        for mark_id in _duplicates(revision.reviewed_mark_ids):
            issues.append(
                ValidationIssue(
                    path=f"audit_log[{index}].reviewed_mark_ids",
                    message=f"duplicate reviewed mark_id '{mark_id}' detected.",
                )
            )
        for signal_id in _duplicates(revision.promoted_signal_ids):
            issues.append(
                ValidationIssue(
                    path=f"audit_log[{index}].promoted_signal_ids",
                    message=f"duplicate promoted signal_id '{signal_id}' detected.",
                )
            )
        for event_id in revision.evidence_event_ids:
            if event_id not in event_id_set:
                issues.append(
                    ValidationIssue(
                        path=f"audit_log[{index}].evidence_event_ids",
                        message=f"unknown event_id '{event_id}'.",
                    )
                )

    for index, tension in enumerate(snapshot.canonical.open_tensions):
        for event_id in _duplicates(tension.source_event_ids):
            issues.append(
                ValidationIssue(
                    path=f"canonical.open_tensions[{index}].source_event_ids",
                    message=f"duplicate source event_id '{event_id}' detected.",
                )
            )
        for event_id in tension.source_event_ids:
            if event_id not in event_id_set:
                issues.append(
                    ValidationIssue(
                        path=f"canonical.open_tensions[{index}].source_event_ids",
                        message=f"unknown event_id '{event_id}'.",
                    )
                )

    return issues


def assert_snapshot_integrity(snapshot: KernelSnapshot) -> None:
    issues = collect_snapshot_issues(snapshot)
    if not issues:
        return

    details = "\n".join(f"- {issue.render()}" for issue in issues)
    raise ContinuityError(
        f"Snapshot validation failed with {len(issues)} issue(s):\n{details}"
    )


def render_snapshot_validation_report(
    snapshot: KernelSnapshot, issues: list[ValidationIssue] | None = None
) -> str:
    resolved_issues = issues if issues is not None else collect_snapshot_issues(snapshot)
    lines = [
        "Snapshot Validation",
        f"status: {'ok' if not resolved_issues else 'invalid'}",
        f"issue_count: {len(resolved_issues)}",
        f"event_count: {len(snapshot.event_log)}",
        f"revision_count: {len(snapshot.audit_log)}",
    ]
    for issue in resolved_issues:
        lines.append(issue.render())
    return "\n".join(lines)
