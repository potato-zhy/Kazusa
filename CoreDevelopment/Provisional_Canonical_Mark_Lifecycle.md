# Provisional Canonical Mark Lifecycle

## Status

Phase 1 research note for the `Core Development Team`.

## Purpose

This note answers one narrow design question:

Does `provisional_canonical_mark` need to exist as an explicit state in the continuity state machine?

Current answer:

yes, but not as a fourth top-level layer.

It should exist as an explicit typed state inside the working layer.

## Problem

Once the project accepts the three-step pattern:

- `record`
- `appraise`
- `canonicalize`

it still needs an answer for a middle class of events.

Some events are:

- too important to treat as ordinary candidate signals,
- not trustworthy enough for immediate canonical admission,
- and too continuity-relevant to allow silent disappearance.

If this middle class has no explicit state, the state machine becomes unstable.

The system is then forced toward one of two bad outcomes:

1. promote too early,
2. or forget too easily.

## Working Judgment

`Provisional canonical mark` should remain an explicit state representation.

But it should be represented:

- inside working state,
- as a review obligation,
- not as canonical identity,
- and not as an independent fourth top-level layer.

This preserves the current three-layer model while still giving the state machine a necessary intermediate form.

## Why It Must Exist Explicitly

### 1. Candidate Signal Is Too Weak

`Provisional_signal` says:

this event may matter.

`Provisional_canonical_mark` says:

this event is not allowed to vanish without explicit review.

Those are not the same claim.

If marks are collapsed into ordinary candidate signals, the system loses the distinction between:

- "possibly relevant"
- and "must later be revisited"

### 2. Audit Alone Is Too Static

An audit record can prove that something once happened.

But audit alone does not create a live forward obligation inside the current working state.

The mark is needed because the system must still carry unresolved review pressure into future integration.

### 3. Canonical Admission Would Be Too Strong

The mark exists precisely for events that are:

- stronger than ordinary candidates,
- weaker than canonical identity admission.

Without this middle state, the system is pushed toward a false binary:

- either canonical now,
- or irrelevant later.

### 4. The State Machine Needs A Stable Pause Position

Not every important event should resolve immediately.

Some events need to be:

- held,
- revisited,
- compared against later evidence,
- and only then resolved.

The mark is the state-machine form of that pause.

## Why It Should Not Become A Fourth Top-Level Layer

Even though it must exist explicitly, it should not become a new top-level state layer.

Reason:

the mark is not a separate domain of being.

It is a typed working-state obligation concerning possible future canonical revision.

If it becomes its own layer, the architecture risks exaggerating its status.

That creates three dangers:

1. `ontological inflation`
   - review obligations start to look like semi-canonical identity facts.
2. `state-machine clutter`
   - too many top-level layers obscure the actual distinction that matters: canonical versus not-yet-canonical.
3. `premature governance complexity`
   - the project begins solving organizational problems that do not yet exist.

So the correct judgment is:

- explicit state: yes,
- separate top-level ontology: no.

## Minimal State-Machine Role

Within the working layer, a `provisional_canonical_mark` plays one role:

it binds a continuity-relevant event to an unresolved review obligation.

That role has five properties.

### 1. Origin

Every mark must originate from:

- one event,
- and usually one candidate signal or equivalent appraisal basis.

It must never appear without traceable source evidence.

### 2. Persistence

Once created, it survives ordinary snapshot progression.

It cannot disappear just because the conversation moved on.

### 3. Non-Canonical Status

It is not itself a canonical self-fact.

The mark means:

review is mandatory.

It does **not** mean:

identity revision has already happened.

### 4. Resolution Requirement

A mark may be cleared only by explicit review.

That review must end in a disposition such as:

- `carry_forward`
- `dismiss`
- `canonicalize`

### 5. Evidence Linkage

Mark review must cite the originating event and any additional evidence used to justify resolution.

Without this, the mark can be manipulated by later framing rather than continuity evidence.

## Minimal Lifecycle

The minimal lifecycle should be:

1. `event recorded`
2. `appraisal performed`
3. `provisional canonical mark created`
4. `ordinary progression carries mark forward`
5. `integration review explicitly resolves mark`

This can be expressed more formally as:

- `none -> mark_open`
- `mark_open -> mark_open` via `carry_forward`
- `mark_open -> cleared_without_admission` via `dismiss`
- `mark_open -> canonical_revision` via `canonicalize`

This is enough for Phase 1.

Nothing more elaborate is yet required.

## What The Mark Is Not

To avoid later confusion, the mark should explicitly not be treated as:

- a memory item,
- a belief,
- a stable trait,
- a canonical relationship fact,
- or an inner realization that already changed identity.

It is a procedural state with developmental significance, not a completed identity claim.

## Why This Matters For Early Construction

The early project is trying to avoid two opposite failures:

1. `single-turn rewrite`
2. `continuity loss through over-conservatism`

`Provisional_canonical_mark` is one of the smallest mechanisms that helps avoid both at once.

It says:

- the event is too important to ignore,
- but not yet trustworthy enough to become identity immediately.

That is exactly the kind of middle discipline a developmental system needs.

## Relation To Immediate Canonical Impact

The mark is especially important because some candidate classes should remain below the immediate-impact threshold.

This includes, in current theory:

- `major relational rupture or commitment` in many cases,
- `constitutive self-recognition`,
- and other events that are structurally important but still interpretation-sensitive.

Without a mark state, these events would have nowhere stable to go.

## Minimal Design Constraints

For Phase 1, the mark system should obey at least these constraints.

1. `rarity`
   - marks should be uncommon and reserved for continuity-relevant material.
2. `explicitness`
   - mark creation must be legible and auditable.
3. `no silent decay`
   - marks should not disappear by timeout alone.
4. `no automatic canonicalization`
   - repeated presence is not by itself enough; review is still required.
5. `no emotional shortcut`
   - intensity alone should not create or resolve a mark without structural grounds.

## What Should Be Deferred

Phase 1 does **not** need to define:

- probabilistic mark confidence,
- automatic expiration windows,
- nested mark hierarchies,
- mark merging across many events,
- or independent mark memory stores.

Those would be premature.

## Open Questions

1. Should repeated related events attach to one existing mark or create several linked marks?
2. Should some mark kinds require stronger review standards than others?
3. When should a dismissed mark leave behind a lasting rationale note?
4. Should relational marks and self-recognition marks eventually receive different subtypes?
5. Can some marks trigger mandatory tension creation in addition to review obligation?

## Working Conclusion

The correct Phase 1 judgment is:

`Provisional canonical mark` should exist as an explicit state in the working layer because the state machine needs a stable, review-bound intermediate form.

But it should **not** become a fourth top-level layer.

That keeps the architecture small while preserving a crucial developmental distinction:

- not everything important is canonical now,
- and not everything non-canonical may be forgotten.
