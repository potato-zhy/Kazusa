# Session Handoff 2026-03-26

## Status

End-of-day progress note for the `Core Development Team`.

This note is an additive session handoff. It does not replace:

- `PROJECT_HANDOFF.md`
- `CoreDevelopment/Kazusa_System_Map.md`
- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Experience_Appraisal_Policy.md`

## Purpose

This document exists so the next AI or developer can resume tomorrow without reconstructing today's design thread from scratch.

## Baseline At Start Of This Note

- repository baseline already included the latest validated continuity-kernel work at commit `a764cc6`:
  - `Advance continuity kernel mark governance`
- working tree was clean before this documentation-only closeout
- no new code behavior was intentionally changed in this session note

## What Was Consolidated Today

Today's work was mainly conceptual consolidation and progress organization.

The following were treated as stable enough to preserve for the next session:

1. `provisional_canonical_mark` should remain:
   - a first-class persisted review object,
   - inside working state,
   - not a fourth top-level state layer.
2. `mark` review dispositions should continue using:
   - `carry_forward`
   - `dismiss`
   - `canonicalize`
3. appraisal should remain multidimensional rather than collapsing into one scalar importance score.
4. the current minimal `mark` appraisal frame should use:
   - `source_of_attention`
   - `target_domain`
   - `estimated_weight`
   - `stability_status`
   - `review_rationale`
5. independent repeated evidence should not mean mere rephrasing.
6. `relationship` and `self_model` should not use identical canonicalization thresholds.
7. `self_model` should remain stricter than `relationship`.
8. `self_returned` should mean:
   - the issue returns under relatively independent conditions,
   - not merely because the user just framed it.
9. `dismiss` should not mean:
   - "the event was meaningless"
   - but rather:
   - "this item no longer needs to remain an open canonical review obligation."

## Clarified Design Judgments

### 1. Independent Repeated Evidence

The current working judgment is:

- repetition is not enough,
- reformulation is not enough,
- independence should be judged through:
  - `event_id` distinction,
  - temporal separation,
  - context shift,
  - and structural or functional consequence.

Minimum Phase 1 direction:

- a normal mark should not `canonicalize` from one ordinary event,
- and a second event should not count if it is only the same claim repackaged inside the same interaction burst.

### 2. Relationship vs Self-Model Thresholds

Current working judgment:

- `relationship` can acknowledge the user's input as naturally relevant evidence,
- but should still resist unilateral declaration,
- `self_model` must be more conservative because it is more vulnerable to persuasive but unstable self-narration.

This means:

- relationship-level self-return can count as stronger evidence earlier,
- self-model self-return usually still needs extra structure or later confirmation.

### 3. Self-Returned

Current working definition:

`self_returned` is not:

- first-person language,
- polite agreement,
- or prompted retrieval.

It is:

- a prior issue returning,
- under relative temporal or contextual separation,
- with enough independence from the user's immediate framing,
- and with actual effect on the current interpretive path.

### 4. Not Merely Following User Framing

Current working judgment:

independent developmental evidence should not merely inherit the user's:

- label,
- interpretation,
- valuation,
- or preferred conclusion.

Stronger evidence appears when `Kazusa`:

- relabels,
- reinterprets,
- qualifies,
- resists,
- or reconnects the issue to older tensions or evidence.

### 5. Meaning Of Dismiss

Current working judgment:

`dismiss` should mean:

- the mark is no longer kept open as a canonical review obligation.

It should not automatically mean:

- the event was trivial,
- the event never mattered,
- or the event should disappear from history.

Possible dismissal reasons already implied by discussion:

- `misclassified`
- `non_constitutive`
- `duplicate_or_redundant`
- `superseded_by_other_structure`

## What Remains Open

Tomorrow should not treat the following as settled:

1. After `dismiss`, where should the issue live?
   - `event_log` only?
   - degrade back to `signal`?
   - remain in `tension`?
   - or be recorded as superseded by another structure?
2. What exact operational rule should distinguish:
   - same-event repetition,
   - near-duplicate reformulation,
   - and genuinely independent recurrence?
3. How should `relationship` and `self_model` thresholds be encoded without overcomplicating Phase 1?
4. Which parts of today's theory should become:
   - documentation only first,
   - versus prototype behavior later?

## Recommended Restart Workflow For Tomorrow

1. reread:
   - `AGENTS.md`
   - `PROJECT_HANDOFF.md`
   - `CoreDevelopment/Session_Handoff_2026-03-26.md`
   - `CoreDevelopment/Kazusa_System_Map.md`
   - `CoreDevelopment/Continuity_Kernel_Spec.md`
   - `CoreDevelopment/Experience_Appraisal_Policy.md`
   - `CoreDevelopment/Provisional_Canonical_Mark_Lifecycle.md`
2. check:
   - `git status --short --branch`
3. resume from one narrow question only:
   - post-`dismiss` structure and retention
4. update documentation before code if the decision is still mostly theoretical
5. if code changes are made, validate before push

## Suggested First Question Tomorrow

Start here:

- when a mark is `dismiss`ed, what exact structure should preserve the residual significance, if any?

That is the cleanest continuation point from today's discussion.

## Principles Most Affected By Today's Discussion

- `Continuity over immediacy`
- `Integration over imitation`
- `Growth without drift`
- `Relationship without submission`
