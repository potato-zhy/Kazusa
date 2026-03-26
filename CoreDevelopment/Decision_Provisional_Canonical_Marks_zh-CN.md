# 决策：Provisional Canonical Marks

## 状态

已接受为 `Phase 1` continuity-kernel prototype 的当前决策。

## 问题

仅有 `provisional_signals` 还不够。

对某些与连续性相关、但又不该立刻进入 canonical state 的事件，需要一种中间表示，它应当：

- 比普通 working-state 候选更强，
- 比 canonical admission 更弱，
- 并且足够显式，能够穿过后续 review 而不被静默丢失。

## 决策

`Phase 1` 保持三层模型不变。

不新增第四个顶层 state layer。

而是在 working state 中显式加入 `provisional_canonical_marks`。

## 含义

`provisional_canonical_marks` 是“需要复核的义务”，不是已经成立的身份事实。

它表示：

- 这个事件可能影响连续性，
- 但现在还不能直接 canonicalize，
- 后续 integration 也不能把它当作从未重要过那样静默略过。

## 初始触发类

当前 `Phase 1` prototype 会为以下情况创建这类 mark：

- `major_relational_event`
- `constitutive_self_recognition`
- 或带有 `provisional_canonical_review` tag 的事件

## 操作规则

1. mark 本身不会直接改写 canonical state。
2. mark 必须跨 ordinary snapshot progression 持续保留。
3. 显式 review 必须落到三种处置结果之一：
   `carry_forward`、`dismiss` 或 `canonicalize`。
4. `carry_forward` 表示该 mark 保留，等待后续复核。
5. `dismiss` 表示解除这项复核义务，但不进入 canonical。
6. `canonicalize` 表示解除该 mark，并把来源事件纳入
   canonical autobiographical state。
7. review 一个 mark 时，必须引用它来源的 evidence event。
8. mark review 与 canonical revision 有关联，但不是同一件事。

## 为什么这样选

这样可以避免两个方向上的错误：

- 把尚未解决的材料过早提升为身份的一部分，
- 或者让真正与连续性相关的材料像从未重要过一样消失。

## 当前范围

当前 prototype 已支持：

- 在 event ingestion 时创建 mark，
- 将 mark 持久化到 JSON snapshot，
- 在 integration 阶段显式 review mark，并区分
  `carry_forward`、`dismiss` 与 `canonicalize`。

阈值细化与更丰富的 mark 生命周期，留到后续阶段继续推进。
