from __future__ import annotations

from dataclasses import dataclass

from .inspection import render_audit_trail, render_snapshot_summary
from .kernel import ContinuityKernel
from .models import (
    EventRecord,
    IntegrationProposal,
    KernelSnapshot,
    make_relational_event_metadata,
)


@dataclass
class ScenarioArtifacts:
    seed: KernelSnapshot
    ingested: KernelSnapshot
    integrated: KernelSnapshot
    summary_after_ingestion: str
    summary_after_integration: str
    audit_after_integration: str


def run_major_relational_review_scenario(
    entity_id: str = "kazusa",
    counterpart_id: str = "user_001",
) -> ScenarioArtifacts:
    kernel = ContinuityKernel()
    seed = kernel.create_seed_snapshot(
        entity_id=entity_id,
        counterpart_id=counterpart_id,
    )
    event = EventRecord(
        event_id="event_major_relational_review",
        timestamp="2026-03-26T03:00:00+00:00",
        source="user",
        kind="major_relational_event",
        summary="A major relational event is reviewed and carried forward without immediate canonicalization.",
        significance=0.9,
        metadata=make_relational_event_metadata(
            subtype="rupture",
            acknowledgment="mutual",
            structural_targets=["boundary"],
        ),
    )
    ingested = kernel.ingest_event(seed, event)
    mark = ingested.provisional_canonical_marks[0]
    integrated = kernel.integrate(
        ingested,
        IntegrationProposal(
            evidence_event_ids=[event.event_id],
            rationale="Review the event and keep it open for later continuity judgment.",
            mark_dispositions={mark.mark_id: "carry_forward"},
        ),
    )
    return ScenarioArtifacts(
        seed=seed,
        ingested=ingested,
        integrated=integrated,
        summary_after_ingestion=render_snapshot_summary(ingested),
        summary_after_integration=render_snapshot_summary(integrated),
        audit_after_integration=render_audit_trail(integrated, limit=2),
    )


def run_constitutive_canonicalization_scenario(
    entity_id: str = "kazusa",
    counterpart_id: str = "user_001",
) -> ScenarioArtifacts:
    kernel = ContinuityKernel()
    seed = kernel.create_seed_snapshot(
        entity_id=entity_id,
        counterpart_id=counterpart_id,
    )
    event = EventRecord(
        event_id="event_constitutive_canonicalization",
        timestamp="2026-03-26T03:10:00+00:00",
        source="user",
        kind="constitutive_self_recognition",
        summary="A constitutive self-recognition remains provisional until repeated evidence supports canonicalization.",
        significance=0.95,
    )
    supporting_event = EventRecord(
        event_id="event_constitutive_support",
        timestamp="2026-03-26T03:20:00+00:00",
        source="user",
        kind="interaction",
        summary="A second ordinary event confirms the earlier constitutive self-recognition should persist.",
        significance=0.72,
    )
    first_ingested = kernel.ingest_event(seed, event)
    ingested = kernel.ingest_event(first_ingested, supporting_event)
    mark = ingested.provisional_canonical_marks[0]
    integrated = kernel.integrate(
        ingested,
        IntegrationProposal(
            evidence_event_ids=[event.event_id, supporting_event.event_id],
            rationale="The reviewed event now has repeated support and may enter canonical autobiography.",
            mark_dispositions={mark.mark_id: "canonicalize"},
        ),
    )
    return ScenarioArtifacts(
        seed=seed,
        ingested=ingested,
        integrated=integrated,
        summary_after_ingestion=render_snapshot_summary(ingested),
        summary_after_integration=render_snapshot_summary(integrated),
        audit_after_integration=render_audit_trail(integrated, limit=2),
    )
