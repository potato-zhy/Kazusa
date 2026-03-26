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

## Open Questions

These are still unresolved and should be treated as active R&D questions:

1. Final definition of `canonical state` fields.
2. Whether `provisional canonical mark` should exist as an explicit state layer.
3. Exact threshold for `major relational rupture or commitment`.
4. Minimum seed structure.
5. Formal significance policy.
6. Sleep / consolidation rules.
7. Constitutional rules for self-revision.

## Recommended Starting Point For The Next Process

Continue `Phase 1 - Continuity Kernel`.

The most productive next step is not broad implementation. It is a short, precise document that defines:

- what belongs in `canonical state`,
- what breaks continuity,
- what is preserved across state revisions,
- and what can never be rewritten in a single turn.
