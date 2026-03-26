# Session Handoff 2026-03-26（中文镜像）

## 状态

这是给 `Core Development Team` 的日终进度交接。

它是补充性的 session handoff，不替代：

- `PROJECT_HANDOFF.md`
- `CoreDevelopment/Kazusa_System_Map.md`
- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Experience_Appraisal_Policy.md`

## 目的

这份文档的作用，是让明天接手的 AI 或开发者不需要重新把今天的理论讨论从头拼起来。

## 本说明开始时的基线

- 仓库代码基线已经包含最新通过验证的 continuity-kernel 工作，提交为 `a764cc6`：
  - `Advance continuity kernel mark governance`
- 在这次仅文档收尾开始前，working tree 是干净的
- 这份 session note 本身不打算改动任何代码行为

## 今天完成了什么整理

今天的工作主要是理论收束和进度整理。

以下内容被视为已经足够稳定，应该保留给下一次继续：

1. `provisional_canonical_mark` 应继续保持为：
   - first-class persisted review object
   - 位于 working state 内
   - 不是第四个顶层 state layer
2. `mark` 的 review disposition 继续保持三类：
   - `carry_forward`
   - `dismiss`
   - `canonicalize`
3. appraisal 应保持多维判断，而不是塌缩成一个标量重要性分数。
4. 当前最小 `mark` appraisal frame 应使用：
   - `source_of_attention`
   - `target_domain`
   - `estimated_weight`
   - `stability_status`
   - `review_rationale`
5. “独立的重复证据”不应等于简单复述。
6. `relationship` 和 `self_model` 不应使用相同的 canonicalization threshold。
7. `self_model` 应比 `relationship` 更保守。
8. `self_returned` 应表示：
   - 该问题在相对独立的条件下再次返回，
   - 而不是因为用户刚刚给了 framing。
9. `dismiss` 不应等于：
   - “这个事件毫无意义”
   - 更准确地说，它表示：
   - “这个项目不再需要作为一个开放的 canonical review obligation 继续保留。”

## 今天澄清的设计判断

### 1. Independent Repeated Evidence

当前工作判断是：

- 仅有重复还不够，
- 仅有改写还不够，
- 是否独立应通过以下方面判断：
  - `event_id` 区分
  - 时间分离
  - 情境变化
  - 结构性或功能性后果

当前最小方向：

- 普通 mark 不应由单个 ordinary event 直接 `canonicalize`
- 第二个事件如果只是同一 interaction burst 里的换壳复述，也不应算独立证据

### 2. Relationship 与 Self-Model 的阈值区别

当前工作判断：

- `relationship` 可以把用户输入视为天然相关的证据来源之一，
- 但仍必须抵抗单方面宣告式改写，
- `self_model` 必须更保守，因为它更容易被“看起来很深刻但并不稳定”的自我叙述污染。

这意味着：

- relationship 类的 self-return 可以更早成为较强证据，
- self-model 类的 self-return 往往还需要额外结构或后续确认。

### 3. Self-Returned

当前工作定义：

`self_returned` 不是：

- 第一人称表达，
- 礼貌性同意，
- 或提示下取回。

它是：

- 一个已有问题再次返回，
- 且具有相对明确的时间或情境分离，
- 与用户当前 framing 有一定独立性，
- 并且真的影响了当前解释路径。

### 4. 不只是顺着用户 Framing 复述

当前工作判断：

独立的发展性证据，不应只是继承用户给出的：

- label
- interpretation
- valuation
- preferred conclusion

更强的证据通常出现在 `Kazusa`：

- 重新命名
- 重新解释
- 加条件
- 抵抗结论
- 或把问题重新连接到旧的 tension / 旧证据

### 5. Dismiss 的含义

当前工作判断：

`dismiss` 应表示：

- 这个 mark 不再作为一个开放的 canonical review obligation 被保留。

它不应自动等于：

- 这个事件很琐碎
- 这个事件从未重要过
- 或这个事件应从历史里消失

目前讨论已经暗含的 dismissal reason 包括：

- `misclassified`
- `non_constitutive`
- `duplicate_or_redundant`
- `superseded_by_other_structure`

## 仍然开放的问题

明天不应把以下内容当成已定结论：

1. 一个 mark 在 `dismiss` 之后，问题应该留在哪里？
   - 只留在 `event_log`？
   - 降回 `signal`？
   - 留在 `tension`？
   - 还是记录为被其他结构吸收？
2. 什么精确操作规则可以区分：
   - 同一事件的重复
   - 近重复改写
   - 真正独立的再次出现
3. `relationship` 与 `self_model` 的不同阈值，怎样写入 Phase 1 才不会过度复杂化？
4. 今天这些理论里，哪些应先写成文档，哪些以后再落到 prototype 行为？

## 明天建议的重启流程

1. 先重读：
   - `AGENTS.md`
   - `PROJECT_HANDOFF.md`
   - `CoreDevelopment/Session_Handoff_2026-03-26.md`
   - `CoreDevelopment/Kazusa_System_Map.md`
   - `CoreDevelopment/Continuity_Kernel_Spec.md`
   - `CoreDevelopment/Experience_Appraisal_Policy.md`
   - `CoreDevelopment/Provisional_Canonical_Mark_Lifecycle.md`
2. 检查：
   - `git status --short --branch`
3. 只从一个窄问题继续：
   - post-`dismiss` 的结构去向与保留方式
4. 如果仍主要是理论问题，先改文档，再考虑代码
5. 如果发生代码改动，验证后再推送

## 明天最适合直接接着做的问题

从这里开始：

- 一个 mark 被 `dismiss` 之后，如果仍残留意义，它应该由什么结构来承接？

这是今天讨论最自然、也最干净的续点。

## 今天最受影响的项目原则

- `Continuity over immediacy`
- `Integration over imitation`
- `Growth without drift`
- `Relationship without submission`
