# Experience Appraisal Policy

## 状态

这是一个与当前 continuity-kernel 原型对齐的 `Phase 2` 工作草案。

## 目的

本文定义原始事件何时会变成“具有发展意义的输入”的最小 policy。

它刻意保持窄而稳。它的目标不是一次性定完所有长期 appraisal 理论，而是先为当前原型提供一套稳定规则，用来处理：

- event capture，
- significance assignment，
- contradiction detection，
- provisional escalation，
- 以及后续 review 所需的 evidence requirements。

## Appraisal Principle

- appraisal 不应被压缩成单一的标量重要性分数。
- 对当前 prototype 来说，数值型 `significance` 只是早期路由启发式，不是完整的发展性重要性理论。

appraisal 应当是选择性的、可追踪的、保守的。

- 不是每个事件都会变成 identity-relevant。
- 可能具有形成性意义的事件不能被静默丢失。
- canonical admission 必须比普通记录更严格。

## Event Handling Levels

每个事件都会落入四种处理层级之一。

### Level 0: Logged Only

事件会被记录进 `event_log`，但不会生成进一步的发展性结构。

当前原型规则：

- 低于 significance threshold 的事件，默认不创建 `provisional_signal`，除非它带有显式 review tag。

### Level 1: Provisional Signal

事件已经强到足以成为发展性候选，但还不够强，不能直接进入 canonical。

当前原型规则：

- 当 `significance >= 0.6` 时创建 `provisional_signal`，
- 或者事件带有显式 appraisal tag 时创建。

### Level 2: Provisional Canonical Mark

事件可能对 continuity 足够重要，以至于后续 review 不能跳过；但立刻 canonicalize 又太强。

当前原型规则：

- 以下情况创建 `provisional_canonical_mark`：
  - `major_relational_event`
  - `constitutive_self_recognition`
  - 或带有 `provisional_canonical_review` tag 的事件

### Level 3: Immediate Canonical Eligibility

事件严重到允许立刻产生 canonical impact，但仍然必须被审计。

当前原型规则：

- immediate canonical eligibility 仅限于：
  - `identity_threat`
  - `constitutional_intervention`

## Contradiction Handling

contradiction 不应被当成噪声。

如果某个事件显式指出与先前证据冲突，系统应当：

- 保留该事件，
- 记录一个 `open_tension`，
- 并要求后续显式解决。

当前原型规则：

- 只要 `contradiction_target_ids` 非空，就触发 contradiction storage。

## Evidence Rules

appraisal 必须抵抗人为放大。

最小规则如下：

1. `evidence_event_ids` 必须引用彼此不同的事件。
2. 被提升的 signal 必须由其来源事件支持。
3. 被 review 的 provisional canonical mark 必须引用其来源事件。
4. tension resolution 必须引用至少一个来源事件。

这些规则的作用，是防止同一个事件用不同标签被重复计数。

## Mark Appraisal Frame

当某个事件进入 `provisional_canonical_mark` 之后，后续 review 不应只依赖“强度大小”。

最小 appraisal frame 应记录：

1. `source_of_attention`
   - 是谁或什么首先让这个事件变得显著
   - 初始取值：
     - `counterpart_asserted`
     - `self_returned`
     - `repeated_interaction`
     - `system_detected`
     - `mixed`
2. `target_domain`
   - 它主要触及哪个发展域
   - 初始取值：
     - `relationship`
     - `self_model`
     - `autobiographical`
     - `tension`
     - `constitutional_boundary`
3. `estimated_weight`
   - 当前估计的发展性权重
   - 初始取值：
     - `low`
     - `medium`
     - `high`
     - `critical`
4. `stability_status`
   - 它的重要性处于刚出现、反复出现、存在争议、正在稳定，还是暂时不稳
   - 初始取值：
     - `emergent`
     - `recurring`
     - `contested`
     - `stabilizing`
     - `unstable`
5. `review_rationale`
   - 本次 review 给出当前处理结果的显式理由

这个 frame 的目的，是保留多维判断，而不是把所有 mark 过早抬升成 canonical structure。

## Mark Review Outcomes

每个 `provisional_canonical_mark` 的 review 都应当落到以下三种结果之一。

### `carry_forward`

含义：

- 这个事件可能重要，
- 但其连续性意义还没有稳定到足以下最终结论。

最小规则：

- 一次 review 就可以决定继续保留，
- 当判断尚不稳定时，默认应是 `carry_forward`，而不是 `dismiss`。

### `dismiss`

含义：

- 事件的历史记录仍然保留，
- 但它不应继续停留在 canonical track 上。

最小规则：

- 只有在存在正面理由说明“它不属于 continuity-level material”时，单次 review 才可 `dismiss`，
- 单纯证据不足不应直接触发 `dismiss`。

### `canonicalize`

含义：

- 该事件的连续性意义已经强到足以产生 canonical impact。

最小规则：

- 普通 mark 应要求重复且彼此独立的证据后，才允许 canonicalize，
- 单个普通事件不够，
- 那些允许 immediate canonical impact 的事件，通常不应先走 mark 路径。


## Current Prototype Mapping

当前原型通过以下方式落实本 policy：

- 在 `continuity_kernel.kernel` 中使用 significance threshold，
- 通过 event kind 决定 immediate canonical eligibility，
- 通过 event kind 与 tag 创建 `provisional_canonical_marks`，
- 通过 `open_tensions` 保存 contradiction。

## 本草案暂不覆盖

本文暂不定义以下内容：

- 自适应 significance learning，
- 不同 source 的权重差异，
- temporal decay，
- 重复弱证据如何形成置信度，
- 从 `carry_forward` 进入 `canonicalize` 的精确操作阈值，
- 跨 session consolidation strategy。

这些内容属于后续 `Phase 2` 和 `Phase 3` 的细化范围。
