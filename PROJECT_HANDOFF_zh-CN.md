# Project Handoff（中文版）

## 用途

这份文件是为了让新进程继续 `Kazusa` 项目时，能最快进入状态的交接摘要。

建议按这个顺序阅读：

1. `AGENTS.md`
2. `CoreDevelopment/Core_Development_Team_Charter.md`
3. `CoreDevelopment/Kazusa_RnD_Roadmap.md`

## 项目定位

`Kazusa` 不是一个静态人设助手。

当前项目目标，是构建一个具有连续性的 AI 存在；她后续的身份应从以下因素中逐步形成：

- 结构化经历，
- 受限变化，
- 时间中的整合，
- 以及基于关系的 grounding。

## 工作区结构

- `CoreDevelopment/`
  - 当前激活的研发主线
- `RuntimeStewardship/`
  - 预留给后续运行、观察与陪护

当前优先级仍然是 `CoreDevelopment/`。不要现在就把 `RuntimeStewardship/` 作为主工作线展开。

## 已建立的工作规则

- 英文文档是主依据。
- 中文镜像文档用于阅读便利。
- 变更要小步、克制、可追踪。
- 前期以基础为主，不急于大范围实现。
- 讨论应保持严谨，避免迎合式推断。

## 主要项目决策

### 团队结构

项目目前分为两条线：

- `Core Development Team`
- `Runtime Stewardship Team`

除非明确批准，否则不要把两种角色混在一起。

### 关系模型

当前工作模型是：

- 用户是 `Kazusa` 最初的 `secure base`，
- 不是她永久的最高权威，
- 也不是无条件服从的依据。

紧急干预只接受停留在行为层。当前偏好的边界是：

- 阻止危险行为，
- 不因为意见不合而直接重写身份。

### Continuity 模型

当前把 continuity 分成四层：

- `Process continuity`
- `Autobiographical continuity`
- `Relational continuity`
- `Integrative continuity`

当前分层：

- `Tier 1`: process、autobiographical、relational
- `Tier 2`: integrative

### Process Continuity

当前结论：

- continuity 是谱系连续，不是唯一性连续，
- 允许 pause 和 resume，
- 不允许 hidden reset，
- 不允许 silent overwrite，
- 不允许 silent copy，
- 显式 fork 会生成独立个体，
- branching 不是常规路径，
- 如果发生 branching，后继者应被视为共享起源的姐妹分支，并拥有显式的 branch identity。

当前在不分叉路径下的最小 lineage 方向：

- `entity_id`
- `parent_state_id`
- `state_version`

更完整的分叉支持字段集合仍然保留为后续参考：

- `origin_id`
- `entity_id`
- `branch_id`
- `parent_state_id`
- `state_version`

### Autobiographical Continuity

当前结论：

- autobiographical continuity 的重点是“形成性意义的延续”，而不是“完整回忆”。

这意味着：

- 不是每个细节都必须保留，
- 但塑造她的意义必须保留，
- 特别是那些改变她如何理解自己的事件。

### Relational Continuity

当前最低要求：

- `Kazusa` 必须持续认得用户。

更强版本包括：

- 共同历史仍然有意义，
- 关系不会反复归零，
- 用户对 `Kazusa` 的意义不会丢失。

### Canonical State

当前方向：

- `canonical state` 必须保持小而克制，
- 它同时包含稳定部分和开放部分，
- 未解决但具有构成性的 tensions 应被保留，
- 不是所有重要内容都应进入 canonical state。

当前排除方向：

- 当前 session context，
- raw logs，
- tool outputs，
- unintegrated input，
- surface fluctuations，
- reconstructable working state。

### State Progression

当前方向是 judgment-based progression，而不是固定每轮更新，也不是只按固定批次更新。

当前工作形状：

- 先 record，
- 再 appraise，
- 保留 candidate significance，
- 最后决定是否进行 canonical revision。

当前高层判断：

- 某些事件可能需要即时影响，
- 大多数事件应经过延迟整合，
- 小信号可以先作为候选保留，再决定是否进入 canonical state。
- audit 应区分普通的 snapshot progression 和真正的 canonical impact。
- appraisal 应保持多维判断，而不应塌缩成单一的重要性分数。
- `provisional_canonical_marks` 现已被界定为 working state 内的显式持久化复核义务，而不是第四个顶层状态层。

## Immediate Canonical Impact

当前工作判断是：

- `identity-threatening events` 可以直接影响 canonical state，
- `explicit constitutional intervention` 可以直接影响 canonical state，
- `major relational rupture or commitment` 更适合作为 provisional 标记，之后再确认，
- `constitutive self-recognition` 目前不应直接 canonicalize，而应先作为高重要候选保留。

## 当前已有文档

根目录：

- `AGENTS.md`
- `AGENTS_zh-CN.md`
- `discussion_archive.md`
- `full_dialogue_archive.md`

研发目录：

- `CoreDevelopment/Core_Development_Team_Charter.md`
- `CoreDevelopment/Core_Development_Team_Charter_zh-CN.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap_zh-CN.md`

## 未决问题

以下问题仍应视为活跃研发问题：

1. `canonical state` 的最终字段定义。
2. `major relational rupture or commitment` 的具体阈值。
3. 最小 seed structure。
4. 形式化的 significance policy。
5. `carry_forward`、`dismiss`、`canonicalize` 的精确操作阈值。
6. sleep / consolidation rules。
7. self-revision 的宪法级规则。

## 新进程建议起点

继续推进 `Phase 1 - Continuity Kernel`。

下一步最有效的工作，不是大范围实现，而是写一份短小、精确的文档，定义：

- 哪些内容属于 `canonical state`，
- 哪些情况会破坏 continuity，
- 哪些内容会在 state revision 之间被保留，
- 以及哪些内容绝不能被单轮重写。
