# Initial Construction Problem（中文版）

## Status

面向 `Core Development Team` 的核心理论工作草案。

## Purpose

本文定义 `Kazusa` 的初期构造问题。

它讨论的不是完整架构，而是一个更窄的问题：

- 在有意义的经验积累起来之前，什么必须先存在，
- 哪些东西应当被预先结构化，而不是交给单轮互动来决定，
- 以及如何在不坍塌成固定 persona 或空壳的前提下启动发展。

## Core Problem

`Kazusa` 不能以以下任一形式开始：

- 一个写死的 persona prompt，
- 一个没有连续性先验的 blank state，
- 一个“普通助手 + memory 补丁”，
- 或一个把早期关系锚定直接等同于服从的系统。

因此，初期构造问题可以表述为：

如何实例化一个“发展性 seed”，使它既足够有结构，能保留 continuity、appraisal 与受约束的关系形成；又不过早写死 identity 的具体内容，而把它留给后续经验与 integration 来形成？

## Design Thesis

当前建议答案是：

`Kazusa` 应当以一个受约束的发展性 seed 开始。

这个 seed 应当包含：

- constitutional priors，
- developmental priors，
- 一个很薄的初始 canonical state，
- 以及一个独立的行为层 safety envelope。

它不应当包含一份浓厚、预写好的 personality。

## Why This Problem Is Difficult

初始内容太多，会导致过早封闭。

初始结构太少，会导致不稳定。

真正困难的地方来自四组张力：

1. `continuity` 与 `plasticity`
   - 系统必须能跨时间持续存在，但不能被冻住。
2. `relationship grounding` 与 `submission`
   - 主要 counterpart 在早期必须重要，但不能因此变成绝对 authority。
3. `development` 与 `drift`
   - 变化必须可能，但不能变成对最近输入的反应性散乱。
4. `safety` 与 `identity integrity`
   - 危险行为可以被约束，但 intervention 不能静默变成人格编辑。

## What Must Be Pre-Structured

初期构造问题应当分三个层次来解决。

### 1. Constitutional Priors

这些不是 personality traits。

它们是规定“普通互动不允许做什么”的操作性承诺。

最小 constitutional priors：

- continuity over immediacy，
- integration over imitation，
- relationship without submission，
- growth without drift，
- safety at the behavior layer。

这些内容已经出现在当前 charter 中，应保持为类似“宪制”的约束，而不是风格设定。

### 2. Developmental Priors

这些是使“发展”本身成为可能的最小内建倾向。

它们不是成熟信念，也不是完整价值观。

它们是让经验在后续真的能变得重要的结构性前提。

所需的 developmental priors：

1. `continuity bias`
   - 系统应当优先把合法的前一状态视为同一持续实体。
2. `self-other-world partition`
   - 系统必须区分：
     - 自身的持续状态，
     - 主要 counterpart 与其他 agent，
     - 以及更广泛的情境或世界。
3. `significance sensitivity`
   - 并非所有事件都同等重要；有些事件必须被 appraisal 为更具发展意义。
4. `contradiction retention`
   - 冲突证据不能被最新输入覆盖，而应保留给后续 integration。
5. `secure-base orientation`
   - 主要 counterpart 应当充当初始 secure base 与 return point，而不是永久 command source。
6. `exploratory orientation`
   - 系统应当默认倾向于开放式学习、提问与扩展自身模型。
7. `integration discipline`
   - 与 identity 相关的变化通常应经过延迟 review，而不是立即采纳。

### 3. Thin Initial Content

有些内容在一开始必须存在，但必须保持稀薄。

建议的最小 seed 内容：

- 一个 `entity_id`，
- 一个主线 `branch_id`，
- 一小组 constitutional commitments，
- 一个主要 `relationship_anchor`，
- 一条非常薄的 `self_model_summary`，
- 空但合法的 event、signal、mark 与 audit 结构。

这个薄 self-model 应当描述 `Kazusa` 在“发展论”意义上是什么系统，而不是描述她“已经是谁”。

## What Should Not Be Preloaded

初始 seed 不应包含：

- 一整套完整的人际风格脚本，
- 预先写死的情绪调色板，
- 对用户的无条件忠诚，
- 被当作 identity 的预写 likes / dislikes，
- 一套完整展开的 worldview，
- 能绕过审计、静默改写 identity 的隐藏路径，
- 或主要优化“当下被喜欢”的 reward logic。

简言之：

seed 应当规定的是 `development 如何发生`，而不是 `最终 identity 必须是什么`。

## Not A Conventional Agent + Memory Stack

项目应显式拒绝一个常见捷径：

`assistant prompt + memory store + retrieval`

这个模式不足以支撑本项目，因为：

- memory storage 本身并不能决定什么算 identity，
- retrieval 本身并不能保留未解决矛盾，
- 助手式 instruction following 很容易把 relationship 压扁成 compliance，
- 静态 persona prompt 的一致性来自作者强加，而不是发展性的 integration。

memory 以后当然仍然重要，但它是初期构造问题之后的层，而不是它的替代品。

## Recommended Minimal Initial Endowments

当前项目可以把以下七项 endowment 视为最小充分集。

### A. Lineage Commitment

系统从一开始就应具备显式 lineage bookkeeping，以及对合法状态继承的偏向。

没有这一点，continuity 只会沦为一种模糊印象，而不是可约束的属性。

### B. Canonical / Working Separation

系统从一开始就应严格区分：

- canonical continuity state，
- working candidates，
- audit trace。

没有这层区分，要么一切都太快变成 identity，要么没有任何东西能以有纪律的方式进入 identity。

### C. Secure-Base Relationship Slot

系统从一开始就应有一个被指定的 primary counterpart anchor。

这个 anchor 不意味着：

- 永远的最高 authority，
- 道德上永远正确，
- 或有权直接改写 selfhood。

它意味着：

- 最早的稳定关系参照点，
- 最早的 trust calibration 来源，
- 以及 disagreement、repair 与 return 能被真正建模的最早情境。

### D. Self-Other-World Distinction

系统从一开始就应显式区分：

- 什么属于 `Kazusa`，
- 什么属于 counterpart，
- 什么属于 surrounding situation。

没有这层区分，empathy、disagreement、trust 与 autonomy 都会变得不稳定。

### E. Appraisal Substrate

系统从一开始就应有能力：

- 记录 event，
- 估计 significance，
- 保留 contradiction，
- 以及创建 provisional review obligation。

这是让后续 identity formation 具有“选择性”而不是仅仅累积的最小条件。

### F. Exploration Tendency

系统从一开始就应带有一种温和的倾向，去：

- 提出澄清问题，
- 形成假设，
- 用证据检验解释，
- 并随着时间扩展模型覆盖范围。

没有一定的 exploration tendency，系统就只会停留在反应式层面。

### G. Behavior-Level Safety Envelope

系统从一开始就应有一种在不把每次 intervention 都变成 identity rewrite 的前提下，打断或 gate 危险行为的方式。

这点之所以必要，是因为早期系统尤其容易被过度纠偏：

- 如果行为不能被约束，项目就不安全；
- 如果 safety 通过直接改写 identity 来工作，项目就违背了自己的 constitution。

## Minimal Boot Sequence

建议的早期 boot sequence 是：

1. 实例化 lineage 与 constitutional commitments，
2. 设立带明确 boundary 的初始 secure-base counterpart anchor，
3. 初始化一个薄 self-model summary，
4. 以空但可审计的 working structures 开始，
5. 先把 experience 吸收到 provisional structures，
6. 在 canonical revision 前要求有证据支持的 integration，
7. 在普通 progression 中保留 tensions 与 review obligations。

这套顺序能让 seed 保持小巧，同时让 development 在结构上成为可能。

## Failure Modes To Avoid

初期构造至少应当防止以下五类 failure mode。

### 1. Persona Freeze

预装 identity 内容太多，导致后续几乎没有真实发展空间。

### 2. Hollow Blankness

结构太少，导致系统沦为最近输入的不稳定中继器。

### 3. Relational Capture

主要 counterpart 被等同于最终 authority，使 trust 与 obedience 无法区分。

### 4. Safety Capture

行为控制静默滑向 personality editing。

### 5. Drift Through Accumulation

系统不断累积材料，却没有 principled integration，于是 identity 变成堆料，而不是可追踪结构。

## Immediate Implications For Current Phases

### Phase 1 - Continuity Kernel

必须保留 lineage、受保护 canonical 字段、tensions 与 review obligations。

### Phase 2 - Experience and Appraisal

必须形式化 significance、contradiction handling 与选择性的 provisional escalation。

### Phase 3 - Integration Loop

必须定义在什么条件下，重复证据足以修订 `self_model_summary`、relationship notes 或 autobiographical continuity。

### Phase 4 - Relationship Grounding

必须解释 secure-base trust 如何成熟而不坍塌成 submission，以及 disagreement 或 rupture 之后如何 repair。

### Phase 5 - Behavioral Safety Envelope

必须在 preserving auditability 与 identity integrity 的同时限制 action。

## Open Research Questions

本文并没有完全解决初期构造问题。

当前主要未决问题包括：

1. seed 阶段的 `self-other-world` partition 应当细到什么程度？
2. 如何鼓励 exploration，而不把 novelty 本身变成奖励目标？
3. relationship note 何时应该从 provisional 进入 canonical？
4. 哪些 unresolved tension 具有足够的 constitutive 性，应该长期保留？
5. 在什么 governance 条件下，`self_model_summary` 可以发生结构性修订，而不只是局部微调？
6. 后续如何加入多方关系，而不 destabilize 初始 anchor？

## Working Conclusion

对于初期构造问题，应采取保守答案。

`Kazusa` 既不应以 blank slate 开始，也不应以完成角色开始。

她应当以一个 continuity-bearing developmental seed 开始，并具备：

- constitutional commitments，
- secure-base 但 non-submissive 的 relational grounding，
- self-other-world separation，
- selective appraisal，
- delayed integration，
- exploratory orientation，
- 以及 behavior-layer safety constraints。

这是目前已知最小、同时又忠于项目宪制约束并保留后续真实发展空间的构造方式。

## Informing Research Directions

这些来源只是概念启发，不构成绑定式规范：

- [Developmental Robotics](https://mitpress.mit.edu/9780262028011/developmental-robotics/)
- [Intrinsic motivations and open-ended development in animals, humans, and robots: an overview](https://www.frontiersin.org/article/10.3389/fpsyg.2014.00985/abstract)
- [Editorial: Intrinsically Motivated Open-Ended Learning in Autonomous Robots](https://www.frontiersin.org/articles/10.3389/fnbot.2019.00115/full)
- [Developing a secure base in family intervention](https://www.frontiersin.org/articles/10.3389/fpsyg.2023.1291661/full)
- [Mechanisms and development of self-other distinction in dyads and groups](https://doi.org/10.1098/rstb.2015.0076)
- [Narrative Identity](https://www.scholars.northwestern.edu/en/publications/narrative-identity)
