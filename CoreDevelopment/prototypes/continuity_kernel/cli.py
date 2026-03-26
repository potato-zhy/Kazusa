from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .inspection import render_audit_trail, render_snapshot_summary
from .kernel import ContinuityKernel
from .models import EventRecord, IntegrationProposal, TensionRecord
from .persistence import load_snapshot, save_snapshot, snapshot_from_dict
from .validation import assert_snapshot_integrity, render_snapshot_validation_report


def event_from_dict(payload: dict[str, Any]) -> EventRecord:
    return EventRecord(**payload)


def integration_proposal_from_dict(payload: dict[str, Any]) -> IntegrationProposal:
    add_tensions = [
        TensionRecord(**tension_payload)
        for tension_payload in payload.get("add_tensions", [])
    ]
    return IntegrationProposal(
        evidence_event_ids=payload["evidence_event_ids"],
        rationale=payload["rationale"],
        promote_signal_ids=payload.get("promote_signal_ids", []),
        reviewed_mark_ids=payload.get("reviewed_mark_ids", []),
        mark_dispositions=payload.get("mark_dispositions", {}),
        revised_self_model_summary=payload.get("revised_self_model_summary"),
        relationship_notes_to_add=payload.get("relationship_notes_to_add", []),
        add_tensions=add_tensions,
        resolved_tensions=payload.get("resolved_tensions", {}),
    )


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def handle_create_seed(args: argparse.Namespace) -> int:
    kernel = ContinuityKernel()
    snapshot = kernel.create_seed_snapshot(
        entity_id=args.entity_id,
        counterpart_id=args.counterpart_id,
        branch_id=args.branch_id,
        self_model_summary=args.self_model_summary,
    )
    save_snapshot(args.output, snapshot)
    print(render_snapshot_summary(snapshot))
    return 0


def handle_summary(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.snapshot)
    print(render_snapshot_summary(snapshot))
    return 0


def handle_audit(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.snapshot)
    print(render_audit_trail(snapshot, limit=args.limit))
    return 0


def handle_validate(args: argparse.Namespace) -> int:
    snapshot = snapshot_from_dict(load_json(args.snapshot))
    assert_snapshot_integrity(snapshot)
    print(render_snapshot_validation_report(snapshot, issues=[]))
    return 0


def handle_ingest_event(args: argparse.Namespace) -> int:
    kernel = ContinuityKernel()
    snapshot = load_snapshot(args.snapshot)
    event = event_from_dict(load_json(args.event_json))
    updated = kernel.ingest_event(snapshot, event)
    save_snapshot(args.output, updated)
    print(render_snapshot_summary(updated))
    return 0


def handle_integrate(args: argparse.Namespace) -> int:
    kernel = ContinuityKernel()
    snapshot = load_snapshot(args.snapshot)
    proposal = integration_proposal_from_dict(load_json(args.proposal_json))
    updated = kernel.integrate(snapshot, proposal)
    save_snapshot(args.output, updated)
    print(render_snapshot_summary(updated))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="continuity-kernel",
        description="Operate the Kazusa continuity-kernel prototype from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_seed = subparsers.add_parser(
        "create-seed",
        help="Create a new continuity-kernel seed snapshot.",
    )
    create_seed.add_argument("output", help="Path to write the seed snapshot JSON.")
    create_seed.add_argument("--entity-id", default="kazusa")
    create_seed.add_argument("--counterpart-id", default="primary_user")
    create_seed.add_argument("--branch-id", default="main")
    create_seed.add_argument("--self-model-summary")
    create_seed.set_defaults(handler=handle_create_seed)

    summary = subparsers.add_parser(
        "summary",
        help="Render a compact snapshot summary.",
    )
    summary.add_argument("snapshot", help="Path to a snapshot JSON file.")
    summary.set_defaults(handler=handle_summary)

    audit = subparsers.add_parser(
        "audit",
        help="Render the recent audit trail for a snapshot.",
    )
    audit.add_argument("snapshot", help="Path to a snapshot JSON file.")
    audit.add_argument("--limit", type=int, default=5)
    audit.set_defaults(handler=handle_audit)

    validate = subparsers.add_parser(
        "validate",
        help="Run structural integrity checks against a snapshot.",
    )
    validate.add_argument("snapshot", help="Path to a snapshot JSON file.")
    validate.set_defaults(handler=handle_validate)

    ingest_event = subparsers.add_parser(
        "ingest-event",
        help="Ingest an event JSON into an existing snapshot.",
    )
    ingest_event.add_argument("snapshot", help="Input snapshot JSON path.")
    ingest_event.add_argument("event_json", help="Event JSON path.")
    ingest_event.add_argument("output", help="Output snapshot JSON path.")
    ingest_event.set_defaults(handler=handle_ingest_event)

    integrate = subparsers.add_parser(
        "integrate",
        help="Apply an integration proposal JSON to an existing snapshot.",
    )
    integrate.add_argument("snapshot", help="Input snapshot JSON path.")
    integrate.add_argument("proposal_json", help="Integration proposal JSON path.")
    integrate.add_argument("output", help="Output snapshot JSON path.")
    integrate.set_defaults(handler=handle_integrate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
