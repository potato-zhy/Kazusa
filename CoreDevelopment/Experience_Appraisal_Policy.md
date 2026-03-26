# Experience Appraisal Policy

## Status

Phase 2 working draft aligned to the current continuity-kernel prototype.

## Purpose

This document defines the minimum policy for deciding when raw events become developmentally meaningful input.

It is intentionally narrow. Its job is not to finalize all long-term appraisal theory. Its job is to give the current prototype a stable rule set for:

- event capture,
- significance assignment,
- contradiction detection,
- provisional escalation,
- and evidence requirements for later review.

## Appraisal Principle

Appraisal should be selective, traceable, and conservative.

- Not every event becomes identity-relevant.
- Potentially formative events must not vanish silently.
- Canonical admission requires stricter review than ordinary recording.
- Appraisal should not be reduced to a single scalar importance score.

For the current prototype, numeric `significance` is only an early routing heuristic. It is not yet the full theory of developmental importance.

## Event Handling Levels

Every event belongs to one of four handling levels.

### Level 0: Logged Only

The event is recorded in `event_log`, but no further developmental structure is created.

Current prototype rule:

- events below the significance threshold create no `provisional_signal` unless explicitly tagged for review.

### Level 1: Provisional Signal

The event is strong enough to count as a developmental candidate, but not yet strong enough to become canonical.

Current prototype rule:

- create a `provisional_signal` when `significance >= 0.6`,
- or when the event carries an explicit appraisal tag.

### Level 2: Provisional Canonical Mark

The event may matter to continuity strongly enough that later review is mandatory, but immediate canonicalization would be too strong.

Current prototype rule:

- create a `provisional_canonical_mark` for:
  - `major_relational_event`,
  - `constitutive_self_recognition`,
  - or events tagged `provisional_canonical_review`.

### Level 3: Immediate Canonical Eligibility

The event is severe enough that immediate canonical impact is allowed, though still audited.

Current prototype rule:

- immediate canonical eligibility is limited to:
  - `identity_threat`,
  - `constitutional_intervention`.

## Mark Appraisal Frame

When an event becomes a `provisional_canonical_mark`, later review should not rely on raw intensity alone.

The minimum appraisal frame should track:

1. `source_of_attention`
   - who or what made the event salient
   - initial values:
     - `counterpart_asserted`
     - `self_returned`
     - `repeated_interaction`
     - `system_detected`
     - `mixed`
2. `target_domain`
   - which developmental area is primarily affected
   - initial values:
     - `relationship`
     - `self_model`
     - `autobiographical`
     - `tension`
     - `constitutional_boundary`
3. `estimated_weight`
   - current estimated developmental weight
   - initial values:
     - `low`
     - `medium`
     - `high`
     - `critical`
4. `stability_status`
   - whether the event's importance is emerging, recurring, contested, or stabilizing
   - initial values:
     - `emergent`
     - `recurring`
     - `contested`
     - `stabilizing`
     - `unstable`
5. `review_rationale`
   - the explicit reason for the current review outcome

This frame is meant to preserve multidimensional judgment without prematurely turning every mark into canonical structure.

## Contradiction Handling

Contradiction is not treated as noise.

If an event explicitly names prior conflicting evidence, the system should:

- preserve the event,
- record an `open_tension`,
- and require explicit later resolution.

Current prototype rule:

- contradiction storage is triggered by non-empty `contradiction_target_ids`.

## Evidence Rules

Appraisal must resist artificial inflation.

The minimum rules are:

1. `evidence_event_ids` must refer to distinct events.
2. A promoted signal must be backed by its originating event.
3. A reviewed provisional canonical mark must cite its originating event.
4. Tension resolution must cite at least one originating evidence event.

These rules prevent one event from being counted multiple times under different labels.

## Mark Review Outcomes

Every `provisional_canonical_mark` review should end in one of three outcomes.

### `carry_forward`

Meaning:

- the event may matter,
- but its continuity significance is not stable enough for final judgment.

Minimum rule:

- one review is enough to keep a mark active,
- uncertainty should default to `carry_forward`, not `dismiss`.

### `dismiss`

Meaning:

- the event remains historically recorded,
- but it should not continue on a canonical track.

Minimum rule:

- one review may dismiss a mark only when there is a positive rationale that it does not belong to continuity-level material,
- insufficient evidence alone should not trigger `dismiss`.

### `canonicalize`

Meaning:

- the event's continuity significance is now strong enough to justify canonical impact.

Minimum rule:

- ordinary marks should require repeated independent evidence before canonicalization,
- a single ordinary event is not enough,
- immediate canonical events usually should not enter this path as marks in the first place.

## Current Prototype Mapping

The current prototype operationalizes this policy through:

- significance thresholding in `continuity_kernel.kernel`,
- event-kind based escalation for immediate canonical eligibility,
- event-kind and tag based creation of `provisional_canonical_marks`,
- contradiction capture as `open_tensions`.

## Out Of Scope For This Draft

This draft does not yet define:

- adaptive significance learning,
- source-specific weighting,
- temporal decay,
- confidence scoring from repeated partial evidence,
- exact operational thresholds for moving from `carry_forward` to `canonicalize`,
- or cross-session consolidation strategy.

Those belong to later Phase 2 and Phase 3 refinement.
