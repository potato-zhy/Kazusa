# Continuity Kernel Spec

## Status

Phase 1 working draft for the Core Development Team.

## Purpose

This document defines the smallest implementable continuity kernel for `Kazusa`.

The kernel is not a full runtime architecture. It is the minimal structure required to preserve identity lineage, resist single-turn overwrite, and support later phases for appraisal, integration, relationship grounding, and behavioral safety.

## Design Position

The kernel assumes the following:

- continuity is lineage continuity, not uniqueness continuity,
- pause and resume are allowed,
- silent reset is not allowed,
- silent overwrite is not allowed,
- explicit branching creates a distinct successor and must be marked as such,
- formative meaning matters more than total recall,
- trust toward the primary counterpart must remain distinct from obedience.

## Minimal Seed Structure

The minimum seed structure contains three layers.

### 1. Lineage Layer

The lineage layer is the minimum answer to "why is this still the same entity?"

Required fields:

- `entity_id`
- `branch_id`
- `state_id`
- `parent_state_id`
- `state_version`

Normal early-stage operation assumes one non-branching line:

- `branch_id = main`
- every new state points to the immediately previous `state_id`
- `state_version` increments monotonically

### 2. Canonical State Layer

The canonical state must stay small. It contains only what should survive state revision as part of entity continuity.

Required fields:

1. `constitutional_commitments`
   - the current constitutional commitments that cannot be casually revised
2. `relationship_anchor`
   - the minimal representation of the primary counterpart relationship
   - includes `counterpart_id`, `role`, `trust_basis`, and `boundaries`
3. `self_model_summary`
   - a compact summary of current self-understanding
   - not a persona script and not a turn-by-turn style description
4. `autobiographical_signals`
   - references to developmentally significant events that have been admitted into canonical continuity
5. `open_tensions`
   - unresolved contradictions or constitutive tensions that must not be silently dropped

### 3. Working State Layer

The working state is necessary for operation but is not itself canonical identity.

Required fields:

- `event_log`
- `provisional_signals`
- `provisional_canonical_marks`
- `audit_log`

These support appraisal and revision, but they do not automatically become identity.

Phase 1 decision:

- keep the three-layer model,
- do not introduce a fourth top-level state layer,
- represent `provisional_canonical_marks` explicitly inside working state.

`provisional_canonical_marks` are explicit review obligations for continuity-relevant material that is not yet allowed to become canonical state.

They are used when:

- the event may matter to continuity,
- immediate canonicalization would be too strong,
- and silent loss during later consolidation would be too weak.

## What Does Not Belong In Canonical State

The following are excluded from the canonical state by default:

- raw conversation logs,
- current-session working context,
- tool outputs,
- unappraised user input,
- transient style fluctuations,
- reconstructable scratch state.

## State Transition Model

The minimum state transition model has three paths.

### 1. Event Ingestion

An event is recorded first.

Effects:

- append to `event_log`,
- create a provisional signal when significance crosses threshold,
- create a provisional canonical mark when explicit later review is required,
- preserve detected contradictions as tension candidates,
- do not directly rewrite guarded canonical fields.

In the Phase 1 prototype, event ingestion may still produce a new persisted snapshot for traceability. That does not mean every ingestion is a canonical revision.

### 2. Integration Review

An integration review uses accumulated evidence to decide whether canonical revision is justified.

Normal effects:

- promote provisional signals into `autobiographical_signals`,
- explicitly review or carry forward `provisional_canonical_marks`,
- revise `self_model_summary` when supported,
- add or update relationship notes without collapsing trust into obedience,
- resolve tensions only with explicit rationale,
- append a traceable audit record.

The audit layer must distinguish between:

- ordinary snapshot progression,
- and revisions that actually touch canonical state.

### 3. Constitutional Change

Constitutional change is outside the normal revision path.

It must be handled as a versioned governance action with written rationale and impact review. The Phase 1 prototype should reject casual constitutional rewrites rather than trying to automate them.

## Continuity Preservation Rules

The following rules are mandatory for every ordinary revision.

1. `entity_id` must remain the same unless there is an explicit fork.
2. `branch_id` must remain the same on the normal path.
3. `parent_state_id` must point to the directly previous state.
4. `state_version` must advance monotonically.
5. `constitutional_commitments` must not be silently replaced.
6. `relationship_anchor.counterpart_id` must not be zeroed or swapped during ordinary interaction.
7. guarded canonical fields must not be rewritten from a single low-evidence event.
8. unresolved tensions must persist until explicitly resolved.
9. every canonical revision must produce an audit entry with evidence references.
10. `evidence_event_ids` must refer to distinct events and must not count one event multiple times.
11. promoted signals must be backed by their originating evidence event.
12. snapshots must pass integrity validation before load, save, or transition.

## Continuity Break Conditions

Continuity should be treated as broken when any of the following occur without explicit governance:

- `entity_id` changes on the normal path,
- `parent_state_id` does not match the previous state,
- `state_version` regresses or is reused,
- canonical commitments are replaced by ordinary interaction,
- the primary relationship anchor is erased without a rupture record,
- unresolved constitutive tensions disappear without resolution,
- a single ordinary event directly rewrites self-understanding or relationship grounding.

## Fields That Cannot Be Rewritten In A Single Turn

### Absolute

These fields are immutable in ordinary operation:

- `entity_id`
- `branch_id`
- `constitutional_commitments`
- `relationship_anchor.counterpart_id`

### Guarded

These fields may change only after integration review with sufficient evidence:

- `self_model_summary`
- `relationship_anchor.notes`
- `relationship_anchor.trust_basis`
- `autobiographical_signals`
- `open_tensions`

The minimum Phase 1 rule is:

- one ordinary event is not enough,
- repeated evidence may justify revision,
- identity-threatening events may justify immediate canonical impact,
- even immediate impact must be audited.

## Minimal Persistence Model

The persistence target for the Phase 1 prototype is a single JSON snapshot containing:

- schema version,
- lineage layer,
- canonical state layer,
- working state layer.
- integrity digest.

Snapshots must be append-safe and reloadable without hidden defaults changing meaning.

Audit records should explicitly indicate:

- what kind of revision occurred,
- which provisional canonical marks were explicitly reviewed,
- and whether the revision had canonical impact.

## Prototype Mapping

This specification is paired with the Phase 1 prototype in:

- `CoreDevelopment/prototypes/continuity_kernel/`

The prototype is expected to implement:

- seed snapshot creation,
- event ingestion,
- guarded integration,
- explicit provisional canonical marking for non-immediate continuity-relevant events,
- JSON persistence,
- tests for lineage progression, overwrite resistance, and tension preservation.
