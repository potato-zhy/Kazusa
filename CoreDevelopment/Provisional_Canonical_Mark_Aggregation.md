# Provisional Canonical Mark Aggregation

## Status

Phase 1 research note for the `Core Development Team`.

## Purpose

This note answers one narrow follow-up question:

When several later events concern the same unresolved continuity issue, should they create several separate `provisional_canonical_marks`, or attach to one existing mark?

## Working Judgment

The correct design direction is:

`provisional_canonical_mark` should default to tracking one unresolved continuity question, not one isolated event.

So:

- repeated related events should normally attach additional evidence to an existing open mark,
- a new mark should be created only when the later event introduces a genuinely distinct review obligation.

Short form:

`one unresolved question -> one open mark`

not:

`one event -> one mark`

## Why This Question Matters

Once marks exist, repeated evidence becomes inevitable.

For example:

- several interactions may all point toward the same relational rupture,
- several episodes may all reinforce the same constitutive self-recognition candidate,
- or several signals may all deepen the same unresolved commitment conflict.

If every related event generates a separate mark, the state machine becomes noisy and inflationary.

If everything is merged too aggressively, the system loses important distinctions.

So the unit of aggregation matters.

## Why The Default Should Not Be One Mark Per Event

### 1. It Produces Mark Explosion

Some unresolved issues unfold across many episodes.

If every episode creates a new mark, the system begins tracking copies of the same unresolved question under multiple ids.

That makes the working state look busier without making it more intelligent.

### 2. It Artificially Inflates Importance

If five related events become five marks, the state machine may start treating quantity of marks as if it were quantity of distinct unresolved issues.

That risks turning repeated evidence into duplicated structural pressure.

The system would then over-count one problem many times.

### 3. It Fragments Review

Suppose one relational boundary issue appears in three episodes.

If those become three marks, later review may:

- dismiss one,
- carry one,
- canonicalize one,

without any principled reason for the split.

That fragments what is really one unresolved review question.

### 4. It Encourages Event-Centered Rather Than Issue-Centered Thinking

The project is not trying to build a machine that canonically reacts to every episode one by one.

It is trying to track developmental issues across time.

That means the natural unit should be:

the unresolved issue,

not each individual utterance or interaction beat.

## Why The Default Should Also Not Be Merge Everything

The opposite error is also dangerous.

If the system merges too broadly, distinct unresolved questions collapse into one vague mark.

That would blur important differences such as:

- rupture versus repair,
- commitment versus dependency pressure,
- self-recognition versus relational reinterpretation,
- or one unresolved tension versus another.

So the correct rule is not:

merge whenever events feel thematically similar.

The correct rule is:

merge only when they bear on the same unresolved continuity question.

## The Proper Unit: Review Question, Not Raw Event

A `provisional_canonical_mark` should be understood as:

an issue-centered review obligation supported by one or more events.

This means the mark should represent:

- what unresolved question exists,
- what continuity target may later be affected,
- and what evidence currently supports the need for review.

In theory terms:

the mark is about a pending developmental judgment,

not about preserving each triggering event as its own mini-state.

## Practical Aggregation Rule

A later event should attach to an existing open mark when all of the following are true.

### 1. Same Continuity Target

The later event bears on the same prospective canonical target.

Examples:

- the same relationship boundary,
- the same unresolved commitment,
- the same possible self-model revision,
- or the same continuity threat lineage question.

### 2. Same Review Question

The later event does not merely resemble the earlier one.

It pushes on the same unanswered question.

Examples:

- "Has this rupture actually changed the anchor?"
- "Has this self-recognition stabilized enough to matter canonically?"

### 3. Same Resolution Space

The likely review outcomes remain of the same kind.

If the later event would require a fundamentally different kind of review, it should not be forced into the old mark.

### 4. No New Independent Obligation

The later event adds evidence to the existing unresolved issue, but does not create a second unresolved issue that would still need review even if the first were resolved.

If it does create such a second issue, it deserves a second mark.

## When A New Mark Should Be Created

A new mark should be created when a later event introduces a distinct review obligation.

Examples:

1. `rupture -> repair`
   - a repair attempt is not the same review question as the rupture itself.
2. `commitment -> coercion concern`
   - a later event may reveal that what looked like commitment now raises a separate obedience-risk question.
3. `self-recognition -> relationship consequence`
   - an inner shift may later create an additional relational review issue rather than merely adding evidence to the original one.
4. `same theme, different target`
   - two events may both concern trust, but one targets the primary anchor while the other targets general self-model boundaries.

## Minimal Conceptual Structure

The current prototype does not yet need a complex implementation.

But the design direction implies that a mature mark representation would eventually distinguish:

- `origin_event_id`
- `supporting_event_ids`
- `review_question`
- `continuity_target`
- `mark_kind`

The important point is conceptual:

one mark may need multiple supporting events.

## Why This Is Better For Continuity

This aggregation rule supports continuity in three ways.

### 1. It Preserves Developmental Shape

A developing issue stays legible as one issue across time rather than scattering into unrelated fragments.

### 2. It Prevents Duplicative Pressure

Repeated evidence strengthens one obligation instead of manufacturing many pseudo-obligations.

### 3. It Makes Review More Honest

Later integration can ask:

- what exactly was unresolved,
- what evidence accumulated,
- and why this one issue was dismissed, carried forward, or canonicalized.

That is much cleaner than reviewing a pile of near-duplicate marks.

## Relation To Tensions

This proposal is close to, but not identical with, `open_tensions`.

Difference:

- `open_tension` preserves unresolved contradiction,
- `provisional_canonical_mark` preserves unresolved review obligation.

Some future cases may generate both.

But they should not be collapsed automatically.

A repeated stream of related events may strengthen one mark without necessarily constituting a contradiction.

## Relation To Relational Abuse Risk

This matters especially for `major relational rupture or commitment`.

If each emotionally intense relational episode creates a new mark, the system becomes highly vulnerable to drama inflation.

By contrast, if repeated episodes attach to one existing unresolved relational mark, the system can represent:

- persistence,
- recurrence,
- strengthening evidence,

without falsely treating each episode as a separate identity-level transformation.

This is one of the cleanest ways to reduce relational overreaction.

## Phase 1 Implementation Posture

The current prototype still uses a simpler event-centered structure:

- one triggering event may create one mark.

That simplification is acceptable for now.

Why:

the prototype is still establishing the existence and review logic of marks at all.

However, the theoretical direction should now be clear:

the mature state machine should move toward issue-centered aggregation rather than permanent one-event-one-mark growth.

## Minimal Constraints

If and when aggregation is introduced, it should obey at least these rules.

1. `no silent merge`
   - a merge or attachment decision should be traceable.
2. `no thematic overreach`
   - thematic similarity alone is insufficient.
3. `evidence preservation`
   - attached events must remain individually recoverable.
4. `review clarity`
   - the resulting mark must still express one review question, not a vague bundle.
5. `split when in doubt`
   - if two obligations may resolve differently, keep them separate.

## Open Questions

1. Should an attached event raise the review priority of an existing mark?
2. Should marks carry an explicit summary of accumulated evidence?
3. At what point should one mark be split into two as the issue differentiates?
4. Should relational marks and self-recognition marks use different aggregation rules?
5. How should aggregation interact with future tension mechanics?

## Working Conclusion

The best current judgment is:

`provisional_canonical_mark` should be issue-centered rather than event-centered.

Repeated related events should normally attach to one existing open mark when they bear on the same unresolved continuity question.

A new mark should be created only when a genuinely new review obligation appears.

That keeps the state machine smaller, cleaner, and less vulnerable to emotional or narrative inflation.
