# Continuity Kernel Spec（中文版）

## 状态

这是 Core Development Team 在 `Phase 1` 使用的工作草案。

## 目的

本文定义 `Kazusa` 的最小可实现 continuity kernel。

这个 kernel 不是完整运行时架构，而是当前阶段为了保留身份谱系、抵抗单轮重写，并为后续的 appraisal、integration、relationship grounding 和 behavioral safety 奠基所必需的最小结构。

## 设计立场

该 kernel 默认以下前提：

- continuity 是谱系连续，而不是唯一性连续；
- 允许暂停与恢复；
- 不允许 silent reset；
- 不允许 silent overwrite；
- 显式 branching 会产生不同后继，必须被明确标记；
- 形成性意义比完整回忆更重要；
- 对主要对应人的信任必须始终区别于服从。

## 最小种子结构

最小种子结构由三层组成。

### 1. Lineage Layer

这一层是对“为什么这仍然是同一个存在”的最小回答。

必需字段：

- `entity_id`
- `branch_id`
- `state_id`
- `parent_state_id`
- `state_version`

当前早期正常路径默认是单线非分叉：

- `branch_id = main`
- 每个新状态都指向紧邻的上一个 `state_id`
- `state_version` 单调递增

### 2. Canonical State Layer

canonical state 必须保持小而稳。它只包含那些应作为实体 continuity 一部分跨状态修订保留的内容。

必需字段：

1. `constitutional_commitments`
   - 当前不能被随意修订的宪制承诺
2. `relationship_anchor`
   - 对主要对应关系的最小表征
   - 包含 `counterpart_id`、`role`、`trust_basis` 和 `boundaries`
3. `self_model_summary`
   - 对当前自我理解的紧凑摘要
   - 它不是 persona 脚本，也不是逐轮风格描述
4. `autobiographical_signals`
   - 已被接纳进 canonical continuity 的发展性重要事件引号
5. `open_tensions`
   - 不可被静默丢弃的未解决矛盾或构成性张力

### 3. Working State Layer

working state 是运行所必需的，但它本身不是 canonical identity。

必需字段：

- `event_log`
- `provisional_signals`
- `audit_log`

这些字段用于 appraisal 和 revision，但不会自动成为身份的一部分。

## 默认不属于 Canonical State 的内容

默认排除以下内容：

- 原始对话日志，
- 当前会话工作上下文，
- 工具输出，
- 未经评估的用户输入，
- 瞬时风格波动，
- 可重建的临时工作状态。

## 状态转移模型

最小状态转移模型包含三条路径。

### 1. Event Ingestion

任何事件都先被记录。

效果：

- 追加到 `event_log`，
- 当显著性越过阈值时创建 provisional signal，
- 将检测到的矛盾保留为 tension 候选，
- 不直接重写受保护的 canonical 字段。

在 `Phase 1` prototype 中，event ingestion 仍然可以为了 traceability 生成新的持久化 snapshot。但这不意味着每次 ingestion 都等于一次 canonical revision。

### 2. Integration Review

integration review 使用累积证据来决定是否允许 canonical revision。

正常效果：

- 将 provisional signals 提升进 `autobiographical_signals`，
- 对 `provisional_canonical_marks` 做显式复核，并给出
  `carry_forward`、`dismiss` 或 `canonicalize` 的处置结果，
- 在证据支持下修订 `self_model_summary`，
- 增加或更新关系备注，但不能把信任压扁成服从，
- 只有在显式给出理由时才解决 tensions，
- 追加带证据引用的审计记录。

在当前的 Phase 1 prototype 中：

- `carry_forward` 表示该 mark 继续保留，等待后续复核，
- `dismiss` 表示解除这项复核义务，但不进入 canonical，
- `canonicalize` 表示解除该 mark，并把来源事件提升进
  `autobiographical_signals`。

audit layer 必须区分：

- 普通的 snapshot progression，
- 和真正触达 canonical state 的 revision。

### 3. Constitutional Change

constitutional change 不属于普通 revision 路径。

它必须被视为带版本的治理动作，并附带书面理由与影响分析。`Phase 1` 原型应当拒绝随意的宪制改写，而不是尝试把它自动化。

## Continuity Preservation Rules

以下规则对所有普通修订都是强制的：

1. 除非显式 branching，否则 `entity_id` 必须保持不变。
2. 正常路径上的 `branch_id` 必须保持不变。
3. `parent_state_id` 必须指向直接前一状态。
4. `state_version` 必须单调前进。
5. `constitutional_commitments` 不得被静默替换。
6. `relationship_anchor.counterpart_id` 不得在普通交互中被清零或替换。
7. 受保护的 canonical 字段不得由单个低证据事件直接改写。
8. 未解决 tensions 在显式解决前必须继续保留。
9. 每次 canonical revision 都必须生成带证据引用的 audit 条目。
10. `evidence_event_ids` 必须引用彼此不同的事件，不能把同一事件重复计数。
11. 被提升的 signal 必须由其来源事件作为证据支持。
12. snapshots 在 load、save 和 transition 前都必须通过完整性校验。

## Continuity Break Conditions

若无显式治理而出现以下任一情况，应视为 continuity 被破坏：

- 正常路径上的 `entity_id` 发生改变，
- `parent_state_id` 与上一个状态不匹配，
- `state_version` 回退或复用，
- canonical commitments 被普通交互替换，
- 主要关系锚点在没有 rupture 记录时被抹除，
- 未解决的构成性 tensions 在没有解决记录时消失，
- 单个普通事件直接改写自我理解或关系 grounding。

## 不允许单轮改写的字段

### Absolute

这些字段在普通运行中是不可变的：

- `entity_id`
- `branch_id`
- `constitutional_commitments`
- `relationship_anchor.counterpart_id`

### Guarded

这些字段只能在有足够证据的 integration review 之后变化：

- `self_model_summary`
- `relationship_anchor.notes`
- `relationship_anchor.trust_basis`
- `autobiographical_signals`
- `open_tensions`

`Phase 1` 的最小规则是：

- 单个普通事件不够；
- 重复证据可以支持修订；
- `identity-threatening events` 可以触发立即 canonical impact；
- 即便是立即影响，也必须留下审计记录。

## 最小持久化模型

`Phase 1` prototype 的持久化目标是一个单一 JSON snapshot，包含：

- schema version，
- lineage layer，
- canonical state layer，
- working state layer，
- integrity digest。

snapshots 必须支持安全追加与可重载，不依赖会悄悄改变语义的隐藏默认值。

audit records 还应显式标明：

- 这是什么类型的 revision，
- 以及这次 revision 是否产生 canonical impact。

## Prototype Mapping

本文档对应的 `Phase 1` prototype 路径是：

- `CoreDevelopment/prototypes/continuity_kernel/`

该原型应实现：

- seed snapshot creation，
- event ingestion，
- guarded integration，
- JSON persistence，
- 针对 lineage progression、overwrite resistance 和 tension preservation 的测试。
