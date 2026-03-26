# Provisional Canonical Mark Lifecycle（中文版）

## Status

面向 `Core Development Team` 的 `Phase 1` 研究说明。

## Purpose

本文只回答一个很窄的设计问题：

`provisional_canonical_mark` 是否需要在 continuity state machine 中作为一种显式状态存在？

当前答案是：

需要，但不应成为第四个 top-level layer。

它应当作为 working layer 内部的一种显式 typed state 存在。

## Problem

一旦项目接受三步结构：

- `record`
- `appraise`
- `canonicalize`

它就必须回答中间那类事件怎么办。

有些事件会同时满足：

- 太重要，不能只当普通 candidate signal，
- 又还不够可靠，不能立刻进入 canonical，
- 同时又与 continuity 太相关，不能允许它静默消失。

如果这类中间状态没有显式表示，state machine 就会变得不稳定。

系统会被迫滑向两个坏结果之一：

1. 过早提升，
2. 或过早遗失。

## Working Judgment

`Provisional canonical mark` 应当继续作为一种显式状态表示保留。

但它应当被表示为：

- working state 的一部分，
- 一种 review obligation，
- 不是 canonical identity，
- 也不是一个独立的第四 top-level layer。

这能在维持当前三层模型的同时，为状态机提供一个必要的中间形式。

## Why It Must Exist Explicitly

### 1. Candidate Signal Is Too Weak

`Provisional_signal` 表示的是：

这个事件“可能重要”。

`Provisional_canonical_mark` 表示的是：

这个事件“不允许在没有显式 review 的情况下消失”。

这两种判断不是一回事。

如果把 mark 折叠进普通 candidate signal，系统就会丢掉以下区分：

- “可能相关”
- 与“必须在之后重新审视”

### 2. Audit Alone Is Too Static

Audit record 能证明某件事曾经发生过。

但 audit 本身不会在当前 working state 中产生一个向前延续的活跃 obligation。

Mark 之所以必要，是因为系统需要把这种未解决的 review pressure 带进未来的 integration。

### 3. Canonical Admission Would Be Too Strong

Mark 的存在，本来就是为了处理这样一类事件：

- 比普通 candidate 更强，
- 比 canonical identity admission 更弱。

没有这个中间状态，系统就会被推向一个假的二元结构：

- 要么现在就 canonical，
- 要么以后就不重要。

### 4. The State Machine Needs A Stable Pause Position

并不是所有重要事件都应该立刻解决。

有些事件需要被：

- 暂时保留，
- 在后续被重新审视，
- 与后来的证据比较，
- 然后再决定怎么解决。

Mark 正是这种“暂停位”的状态机形式。

## Why It Should Not Become A Fourth Top-Level Layer

虽然它必须显式存在，但它不应当变成新的 top-level state layer。

原因是：

mark 不是一个独立的“存在域”。

它只是 working-state 内部、面向未来 canonical revision 的一种 typed obligation。

如果把它抬成独立 layer，架构会高估它的地位。

这会带来三个风险：

1. `ontological inflation`
   - review obligation 看起来会像半个 canonical identity fact。
2. `state-machine clutter`
   - 过多 top-level layers 会遮蔽真正重要的区分：canonical 与 not-yet-canonical。
3. `premature governance complexity`
   - 项目会开始解决一些目前还不存在的组织级问题。

所以正确判断是：

- 作为显式状态存在：要，
- 升成独立 top-level ontology：不要。

## Minimal State-Machine Role

在 working layer 中，`provisional_canonical_mark` 只承担一个角色：

把一个 continuity-relevant event 绑定到一项尚未解决的 review obligation 上。

这个角色有五个属性。

### 1. Origin

每个 mark 都必须来自：

- 一个 event，
- 通常还伴随一个 candidate signal 或等价的 appraisal 基础。

它不能在没有可追踪源证据的情况下凭空出现。

### 2. Persistence

一旦创建，它必须穿过 ordinary snapshot progression 持续存在。

不能因为对话继续往前走，它就自动消失。

### 3. Non-Canonical Status

它本身不是 canonical self-fact。

Mark 的意思是：

这件事必须被 review。

它**不是**在说：

identity revision 已经发生。

### 4. Resolution Requirement

Mark 只能通过显式 review 被清除。

这个 review 必须落到某种 disposition，例如：

- `carry_forward`
- `dismiss`
- `canonicalize`

### 5. Evidence Linkage

对 mark 的 review 必须引用来源事件，以及任何额外用于解决它的证据。

否则，mark 就会被后来的 framing 操纵，而不是由 continuity evidence 驱动。

## Minimal Lifecycle

最小 lifecycle 应当是：

1. `event recorded`
2. `appraisal performed`
3. `provisional canonical mark created`
4. `ordinary progression carries mark forward`
5. `integration review explicitly resolves mark`

如果更形式化地写，就是：

- `none -> mark_open`
- `mark_open -> mark_open` 通过 `carry_forward`
- `mark_open -> cleared_without_admission` 通过 `dismiss`
- `mark_open -> canonical_revision` 通过 `canonicalize`

对于 `Phase 1`，这已经足够。

暂时不需要更复杂的东西。

## What The Mark Is Not

为了避免后续混淆，应明确规定 mark 不应被当成：

- 一条 memory item，
- 一个 belief，
- 一个稳定 trait，
- 一个 canonical relationship fact，
- 或一次已经改变 identity 的内在顿悟。

它是一种具有发展意义的程序性状态，而不是完成的 identity claim。

## Why This Matters For Early Construction

早期项目想避免两个相反的失败：

1. `single-turn rewrite`
2. `continuity loss through over-conservatism`

`Provisional_canonical_mark` 正是同时避免这两种失败的最小机制之一。

它在说：

- 这个事件重要到不能忽略，
- 但又还不够可靠，不能马上变成 identity。

这正是一个 developmental system 所需要的中间纪律。

## Relation To Immediate Canonical Impact

Mark 之所以特别重要，是因为有些候选事件本来就应当留在 immediate-impact threshold 以下。

按当前理论，这包括：

- 许多 `major relational rupture or commitment`，
- `constitutive self-recognition`，
- 以及其他结构上重要、但仍高度依赖解释的事件。

如果没有 mark state，这些事件就没有一个稳定去处。

## Minimal Design Constraints

在 `Phase 1` 中，mark system 至少应满足以下约束。

1. `rarity`
   - mark 应当少见，只保留给 continuity-relevant material。
2. `explicitness`
   - mark 的创建必须清晰、可审计。
3. `no silent decay`
   - mark 不能只靠超时自动消失。
4. `no automatic canonicalization`
   - 即便反复存在，也不能自动升格；仍需 review。
5. `no emotional shortcut`
   - 单靠强烈情绪，既不能创建也不能解决 mark，除非有结构性理由。

## What Should Be Deferred

`Phase 1` **不**需要定义：

- 概率化的 mark confidence，
- 自动过期窗口，
- 嵌套 mark 层级，
- 多事件 mark 合并机制，
- 或独立的 mark memory store。

这些都太早了。

## Open Questions

1. 多个重复相关事件，应附着到同一个已有 mark，还是创建多个彼此关联的 mark？
2. 不同 kind 的 mark，是否应要求不同强度的 review 标准？
3. 一个被 dismiss 的 mark，是否应额外留下持久 rationale note？
4. relational marks 与 self-recognition marks，是否最终应被分成不同 subtype？
5. 某些 mark 是否应在产生 review obligation 的同时，强制创建 tension？

## Working Conclusion

当前 `Phase 1` 的正确判断是：

`Provisional canonical mark` 应当作为 working layer 内的一种显式状态存在，因为状态机需要一个稳定、受 review 约束的中间形式。

但它**不应**升格为第四个 top-level layer。

这样既能保持架构小巧，又能保住一个关键的发展性区分：

- 不是所有重要的东西现在都已经 canonical，
- 也不是所有尚未 canonical 的东西都可以被忘掉。
