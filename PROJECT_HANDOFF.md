# Project Handoff

## Purpose

This file is the shortest reliable handoff for continuing the `Kazusa` project in a new process.

Use this document as the first entry point, then read:

1. `AGENTS.md`
2. `CoreDevelopment/Core_Development_Team_Charter.md`
3. `CoreDevelopment/Kazusa_RnD_Roadmap.md`

## Project Identity

`Kazusa` is not a static persona assistant.

The project goal is to build a continuity-bearing AI entity whose later identity should emerge from:

- structured experience,
- bounded change,
- integration over time,
- and relationship-based grounding.

## Workspace Structure

- `CoreDevelopment/`
  - active R&D track
- `RuntimeStewardship/`
  - reserved for later runtime operations and stewardship

Current priority is `CoreDevelopment/`. Do not start runtime-system work as the main track yet.

## Working Rules Already Established

- English documents are the source of truth.
- Chinese mirror documents may be added for reading convenience.
- Changes should be small and deliberate.
- Early-stage work should focus on foundations, not broad implementation.
- Discussion should remain rigorous and non-sycophantic.

## Major Project Decisions

### Team Structure

Two project tracks are established:

- `Core Development Team`
- `Runtime Stewardship Team`

These roles should not be collapsed together without explicit approval.

### Relationship Model

The current working relationship model is:

- the user is `Kazusa`'s initial secure base,
- not her permanent highest authority,
- and not a justification for unconditional obedience.

Emergency intervention is accepted only at the behavior layer. The preferred boundary is:

- stop dangerous behavior,
- do not directly rewrite identity because of disagreement.

### Continuity Model

Continuity has been split into four layers:

- `Process continuity`
- `Autobiographical continuity`
- `Relational continuity`
- `Integrative continuity`

Current tiering:

- `Tier 1`: process, autobiographical, relational
- `Tier 2`: integrative

### Process Continuity

Current decisions:

- continuity is lineage continuity, not uniqueness continuity,
- pause and resume are allowed,
- hidden reset is not allowed,
- silent overwrite is not allowed,
- silent copy is not allowed,
- explicit fork creates distinct individuals,
- branching is not desired as a normal path,
- if branching occurs, successors should be treated as sister descendants with explicit branch identity.

Current minimal lineage direction for the non-branching path:

- `entity_id`
- `parent_state_id`
- `state_version`

The earlier broader lineage set remains relevant for later branching support:

- `origin_id`
- `entity_id`
- `branch_id`
- `parent_state_id`
- `state_version`

### Autobiographical Continuity

Current decision:

- autobiographical continuity is primarily continuity of significance, not total recall.

This means:

- not every detail must persist,
- but formative meaning must persist,
- especially where events changed how `Kazusa` understands herself.

### Relational Continuity

Current minimum:

- `Kazusa` must continue to recognize the user.

Stronger form:

- shared history remains meaningful,
- the relationship does not repeatedly reset to zero,
- and the user's meaning to `Kazusa` is not lost.

### Canonical State

Current direction:

- `canonical state` must remain small,
- it includes both stable and open parts,
- unresolved but constitutive tensions should be preserved,
- not everything important belongs in canonical state.

Current exclusion direction:

- current session context,
- raw logs,
- tool outputs,
- unintegrated input,
- surface fluctuations,
- reconstructable working state.

### State Progression

Current direction is judgment-based progression, not fixed per-turn progression and not only fixed-batch progression.

Working shape:

- record,
- appraise,
- keep candidate significance,
- then decide on canonical revision.

Current high-level judgment:

- some events may need immediate impact,
- most events should mature through delayed integration,
- small signals may be retained as candidates before canonical adoption.
- audit should distinguish ordinary snapshot progression from true canonical impact.
- appraisal should remain multidimensional rather than collapsing into one importance score.
- `provisional_canonical_marks` now exist as explicit persisted review obligations inside working state, not as a fourth top-level state layer.

## Immediate Canonical Impact

Current working distinction:

- `identity-threatening events` can directly affect canonical state,
- `explicit constitutional intervention` can directly affect canonical state,
- `major relational rupture or commitment` should likely be provisional first, then confirmed,
- `constitutive self-recognition` should not directly canonicalize yet and should remain a high-significance candidate until confirmed.

## Existing Documents

Root:

- `AGENTS.md`
- `AGENTS_zh-CN.md`
- `discussion_archive.md`
- `full_dialogue_archive.md`

Core development:

- `CoreDevelopment/Core_Development_Team_Charter.md`
- `CoreDevelopment/Core_Development_Team_Charter_zh-CN.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap_zh-CN.md`
- `CoreDevelopment/Session_Handoff_2026-03-26.md`
- `CoreDevelopment/Session_Handoff_2026-03-26_zh-CN.md`

## Latest Validated Snapshot

Date:

- `2026-03-26`

Last validated implementation commit:

- `a764cc6` - `Advance continuity kernel mark governance`

Repository state at handoff:

- local `main` is clean,
- local `main` matches `origin/main`,
- prototype and documentation changes below are already pushed.

## Prototype Status

The active continuity-kernel prototype now includes:

- seed snapshot creation with `developmental_priors`,
- guarded event ingestion and guarded integration review,
- JSON persistence with backward-compatible snapshot loading,
- standalone snapshot validation,
- CLI entry points for create / ingest / integrate / summary / audit / validate,
- inspection helpers and example scenarios,
- persisted `provisional_canonical_marks` with explicit review dispositions.

Current validated prototype modules:

- `CoreDevelopment/prototypes/continuity_kernel/models.py`
- `CoreDevelopment/prototypes/continuity_kernel/kernel.py`
- `CoreDevelopment/prototypes/continuity_kernel/persistence.py`
- `CoreDevelopment/prototypes/continuity_kernel/validation.py`
- `CoreDevelopment/prototypes/continuity_kernel/inspection.py`
- `CoreDevelopment/prototypes/continuity_kernel/cli.py`
- `CoreDevelopment/prototypes/continuity_kernel/examples.py`

## What Was Completed In This Cycle

Code and tests now enforce the following:

1. `autobiographical_signals` cannot be revised by a single ordinary event via direct signal promotion.
2. `provisional_canonical_mark` canonicalization cannot admit a single ordinary event into canonical autobiography.
3. `major_relational_event` requires structured metadata and basic anti-abuse validation.
4. `CanonicalState` seeds now include `developmental_priors`.
5. `provisional_canonical_mark` now carries minimal issue-centered structure:
   - `origin_event_id`
   - `supporting_event_ids`
   - `review_question`
   - `continuity_target`
6. Legacy snapshots missing the new mark fields load with deterministic backfill.
7. Repeated `major_relational_event` cases can now attach to one existing open mark when they share:
   - `mark_kind`
   - `review_question`
   - `continuity_target`
8. Reviewing an aggregated open mark must cite all currently attached `supporting_event_ids`.

## Validation Status

Last full validation command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s CoreDevelopment\tests -v
```

Last result:

- `47/47 OK`

## Files Changed In The Latest Development Cycle

Implementation:

- `CoreDevelopment/prototypes/continuity_kernel/__init__.py`
- `CoreDevelopment/prototypes/continuity_kernel/models.py`
- `CoreDevelopment/prototypes/continuity_kernel/kernel.py`
- `CoreDevelopment/prototypes/continuity_kernel/persistence.py`
- `CoreDevelopment/prototypes/continuity_kernel/validation.py`
- `CoreDevelopment/prototypes/continuity_kernel/inspection.py`
- `CoreDevelopment/prototypes/continuity_kernel/cli.py`
- `CoreDevelopment/prototypes/continuity_kernel/examples.py`

Tests:

- `CoreDevelopment/tests/test_continuity_kernel.py`
- `CoreDevelopment/tests/test_continuity_kernel_seed_priors.py`
- `CoreDevelopment/tests/test_continuity_kernel_validation.py`
- `CoreDevelopment/tests/test_continuity_kernel_inspection.py`
- `CoreDevelopment/tests/test_continuity_kernel_cli.py`
- `CoreDevelopment/tests/test_continuity_kernel_examples.py`

Related design documents added or updated:

- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Decision_Provisional_Canonical_Marks.md`
- `CoreDevelopment/Immediate_Canonical_Impact_Policy.md`
- `CoreDevelopment/Initial_Construction_Problem.md`
- `CoreDevelopment/Provisional_Canonical_Mark_Aggregation.md`
- `CoreDevelopment/Provisional_Canonical_Mark_Lifecycle.md`

## Why These Changes Were Made

The main purpose of this cycle was to make Phase 1 more conservative and auditable without making a large architectural jump.

The key theme was:

- keep continuity-relevant material from disappearing,
- prevent single-event ordinary rewrites,
- begin moving marks from event-centered shape toward issue-centered shape,
- and require explicit evidence linkage when marks are reviewed.

## Assumptions Made

These assumptions currently shape the implementation:

1. English documents remain the source of truth.
2. Another process or AI may continue editing theory documents in parallel; reread target files immediately before editing.
3. The current aggregation rule is intentionally narrow.
4. Only `major_relational_event` auto-attaches to an existing mark at present.
5. `constitutive_self_recognition` is still treated more conservatively and does not yet auto-aggregate.
6. Aggregated mark review currently requires all attached supporting evidence for any explicit disposition, including `carry_forward`.

## Immediate Open Questions From This Cycle

These remain active and should not be treated as settled:

1. Whether aggregated mark review should require all attached evidence for every disposition, or only for `dismiss` and `canonicalize`.
2. Whether `constitutive_self_recognition` should later gain a similarly narrow aggregation rule.
3. How formal `fork / rupture / successor` handling should be added for explicit branch creation.
4. How far relational-event schema should go before any broader immediate-impact behavior is allowed.
5. What exact operational thresholds should govern `carry_forward`, `dismiss`, and `canonicalize`.

## Open Questions

These are still unresolved and should be treated as active R&D questions:

1. Final definition of `canonical state` fields.
2. Exact threshold for `major relational rupture or commitment`.
3. Minimum seed structure.
4. Formal significance policy.
5. Exact operational thresholds for `carry_forward`, `dismiss`, and `canonicalize`.
6. Sleep / consolidation rules.
7. Constitutional rules for self-revision.

## Recommended Starting Point For The Next Process

Continue `Phase 1 - Continuity Kernel`.

The best next implementation step should stay narrow and follow the existing prototype rather than opening a new subsystem.

Recommended next coding step:

- improve inspection and CLI visibility for aggregated provisional marks.

Concretely, the next process should:

1. reread:
   - `AGENTS.md`
   - `CoreDevelopment/Core_Development_Team_Charter.md`
   - `CoreDevelopment/Kazusa_RnD_Roadmap.md`
   - `CoreDevelopment/Session_Handoff_2026-03-26.md`
   - `CoreDevelopment/Continuity_Kernel_Spec.md`
   - `CoreDevelopment/Decision_Provisional_Canonical_Marks.md`
   - `CoreDevelopment/Provisional_Canonical_Mark_Aggregation.md`
   - `CoreDevelopment/Provisional_Canonical_Mark_Lifecycle.md`
   - `CoreDevelopment/Immediate_Canonical_Impact_Policy.md`
2. check `git status --short --branch`.
3. reread target files immediately before any edit because concurrent local edits remain possible.
4. make only one small increment.

Preferred next increment:

- expose, in inspection and CLI output:
  - mark `review_question`,
  - mark `continuity_target`,
  - count of `supporting_event_ids`,
  - and whether a proposed review cites full supporting evidence.

After that increment:

1. run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s CoreDevelopment\tests -v
```

2. if GitHub sync is needed, use the already-working SSH-over-443 pattern:

```powershell
git -c core.sshCommand="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -p 443" fetch origin
git -c core.sshCommand="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -p 443" push origin main
```

## Project Principles Most Affected

The latest cycle most directly touched:

- `Continuity over immediacy`
- `Integration over imitation`
- `Growth without drift`
- `Relationship without submission`
