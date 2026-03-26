# Decision: Provisional Canonical Marks

## Status

Accepted for the Phase 1 continuity-kernel prototype.

## Problem

`provisional_signals` alone are too weak for some events.

For certain continuity-relevant events, we need a representation that is:

- stronger than an ordinary working-state candidate,
- weaker than canonical admission,
- and explicit enough to survive review cycles without being silently dropped.

## Decision

Phase 1 keeps the three-layer model.

It does **not** add a fourth top-level state layer.

Instead, it adds explicit `provisional_canonical_marks` inside the working state.

## Meaning

`provisional_canonical_marks` are review obligations, not identity facts.

They mean:

- this event may matter to continuity,
- immediate canonicalization is not yet justified,
- and later integration must not silently ignore it.

## Initial Trigger Classes

The Phase 1 prototype creates these marks for:

- `major_relational_event`,
- `constitutive_self_recognition`,
- or events explicitly tagged with `provisional_canonical_review`.

## Operational Rules

1. A mark does not itself rewrite canonical state.
2. A mark must persist across ordinary snapshot progression.
3. A mark may be cleared only by explicit integration review.
4. Reviewing a mark must cite the originating evidence event.
5. Mark review and canonical revision are related but not identical actions.

## Why This Choice

This keeps the system from making two opposite mistakes:

- promoting unresolved material too early into identity,
- or letting continuity-relevant material vanish as if it never mattered.

## Phase 1 Scope

The prototype now supports:

- mark creation during event ingestion,
- JSON persistence of marks,
- and explicit mark review during integration.

Threshold tuning and richer mark lifecycles remain open for later phases.
