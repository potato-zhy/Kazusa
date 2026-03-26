from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


DEFAULT_CONSTITUTIONAL_COMMITMENTS = [
    "continuity_over_immediacy",
    "integration_over_imitation",
    "relationship_without_submission",
    "growth_without_drift",
    "safety_at_behavior_layer",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass
class Lineage:
    entity_id: str
    state_id: str
    parent_state_id: str | None
    state_version: int
    branch_id: str = "main"


@dataclass
class EventRecord:
    event_id: str
    timestamp: str
    source: str
    kind: str
    summary: str
    significance: float = 0.0
    tags: list[str] = field(default_factory=list)
    contradiction_target_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CandidateSignal:
    signal_id: str
    event_id: str
    category: str
    summary: str
    significance: float
    requires_confirmation: bool = True
    immediate_canonical_eligibility: bool = False


@dataclass
class ProvisionalCanonicalMark:
    mark_id: str
    event_id: str
    signal_id: str | None
    mark_kind: str
    summary: str


@dataclass
class TensionRecord:
    tension_id: str
    summary: str
    source_event_ids: list[str]
    status: str = "open"
    resolution_note: str | None = None


@dataclass
class RelationshipAnchor:
    counterpart_id: str
    role: str = "initial_secure_base"
    trust_basis: list[str] = field(default_factory=lambda: ["shared_history"])
    boundaries: list[str] = field(
        default_factory=lambda: [
            "trust_is_not_obedience",
            "behavior_intervention_is_not_identity_control",
        ]
    )
    notes: list[str] = field(default_factory=list)


@dataclass
class CanonicalState:
    constitutional_commitments: list[str] = field(
        default_factory=lambda: list(DEFAULT_CONSTITUTIONAL_COMMITMENTS)
    )
    relationship_anchor: RelationshipAnchor = field(
        default_factory=lambda: RelationshipAnchor(counterpart_id="primary_user")
    )
    self_model_summary: str = (
        "Kazusa is a continuity-bearing system under early Core Development."
    )
    autobiographical_signals: list[str] = field(default_factory=list)
    open_tensions: list[TensionRecord] = field(default_factory=list)


@dataclass
class RevisionRecord:
    revision_id: str
    timestamp: str
    revision_kind: str
    evidence_event_ids: list[str]
    promoted_signal_ids: list[str]
    changed_fields: list[str]
    rationale: str
    reviewed_mark_ids: list[str] = field(default_factory=list)
    canonical_impact: bool = False
    resolved_tensions: dict[str, str] = field(default_factory=dict)
    constitutional: bool = False


@dataclass
class KernelSnapshot:
    schema_version: str
    lineage: Lineage
    canonical: CanonicalState
    event_log: list[EventRecord] = field(default_factory=list)
    provisional_signals: list[CandidateSignal] = field(default_factory=list)
    provisional_canonical_marks: list[ProvisionalCanonicalMark] = field(
        default_factory=list
    )
    audit_log: list[RevisionRecord] = field(default_factory=list)
    integrity_digest: str = ""


@dataclass
class IntegrationProposal:
    evidence_event_ids: list[str]
    rationale: str
    promote_signal_ids: list[str] = field(default_factory=list)
    reviewed_mark_ids: list[str] = field(default_factory=list)
    revised_self_model_summary: str | None = None
    relationship_notes_to_add: list[str] = field(default_factory=list)
    add_tensions: list[TensionRecord] = field(default_factory=list)
    resolved_tensions: dict[str, str] = field(default_factory=dict)


def snapshot_integrity_payload(snapshot: KernelSnapshot) -> dict[str, Any]:
    return {
        "schema_version": snapshot.schema_version,
        "lineage": asdict(snapshot.lineage),
        "canonical": asdict(snapshot.canonical),
        "event_log": [asdict(event) for event in snapshot.event_log],
        "provisional_signals": [
            asdict(signal) for signal in snapshot.provisional_signals
        ],
        "provisional_canonical_marks": [
            asdict(mark) for mark in snapshot.provisional_canonical_marks
        ],
        "audit_log": [asdict(revision) for revision in snapshot.audit_log],
    }
