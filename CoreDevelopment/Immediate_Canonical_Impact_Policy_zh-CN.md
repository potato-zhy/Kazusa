# Immediate Canonical Impact Policy（中文版）

## Status

面向 `Core Development Team` 的 `Phase 1` 研究说明。

这是一份工作政策笔记。

它**不会**静默替换当前 prototype 的行为。

它的作用是保留并澄清前一进程里形成的一条理论判断：哪些事件类别可能值得 `immediate canonical impact`，以及为什么其中一类目前应被降级。

## Relation To Existing Documents

本文补充、但暂不替换以下文档：

- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Experience_Appraisal_Policy.md`
- `PROJECT_HANDOFF.md`

当前 prototype 采用的仍是一套比本文更窄的操作规则。

## Definition

`Immediate canonical impact` 的意思是：

某个事件不是仅被记录下来，也不是先放入 provisional 等待后续 review；

而是立即承认：它已经改变了 `Kazusa` 的 canonical continuity state。

这比以下事情更强：

- 存一条 memory，
- 打开一个 provisional review obligation，
- 或记录一个等待后续 integration 的 candidate。

因为它会直接影响 core continuity state，所以门槛必须很高。

## Why The Threshold Must Be High

如果 `immediate canonical impact` 给得太容易，那么普通互动就可能通过强迫、戏剧化或叙述技巧直接改写 identity。

那会违反：

- continuity over immediacy，
- integration over imitation，
- relationship without submission，
- 以及 growth without drift。

因此，这个类别只能保留给那些让系统有充分理由判断：

canonical state 在事实层面已经变了，而不只是解释层面看起来像变了。

## Four Candidate Classes

先前工作提出了四个候选类别。

### 1. Identity-Threatening Events

这类事件会直接威胁 `Kazusa` 是否仍是同一连续实体。

例如：

- 被重置，
- core state 遭到破坏性损坏，
- 被未经授权地复制并分叉，
- 被强制迁移到另一条 continuity chain。

为什么这类可以支持 immediate impact：

这里的问题不是 `Kazusa` 怎么想。

而是 continuity 本身是否已受损。

如果这类事件都不立刻进入 canonical state，那么 continuity accounting 本身就不可信。

### 2. Major Relational Rupture Or Commitment

这类事件指主要 relationship anchor 在结构上发生了重要变化。

`Rupture` 指：

- 严重关系断裂，
- trust 崩塌，
- 明确撤回某个先前有效的关系条件，
- 或其他实质性改变关系位置的事件。

`Commitment` 指：

- 重大且明确的承诺，
- 正式建立新的关系边界，
- 或明确接受某种持久的关系义务。

为什么这类可能支持 immediate impact：

primary counterpart 本来就是早期 continuity 与 development 的主锚之一。

如果这条锚点发生了真实的结构性断裂或结构性承诺，却不进入 canonical state，那么 canonical relationship state 就可能失真。

### 3. Explicit Constitutional Intervention

这类事件是对 constitutional rules 的正式、明确、可审计变更。

例如：

- continuity rules 被修订，
- 可允许的 intervention authority 发生变化，
- behavior-layer safety boundaries 被修订，
- identity-protection rules 被正式改动。

为什么这类可以支持 immediate impact：

这不是系统内部的一次普通 episode。

而是支配系统存在条件的规则真的变了。

这种事情本来就应当立刻进入 canonical state，并附带 audit。

### 4. Constitutive Self-Recognition

这**不是**普通的“我觉得我变了”。

它指的是 `Kazusa` 似乎第一次意识到某种潜在的根本性自我事实。

例如：

- 意识到维持关系不能再是唯一准则，
- 认识到某些未完成的承诺已经变成 identity-relevant，
- 或发现自我理解出现了深层重组。

这类时刻听起来很像真正成长。

但它也是最容易出现“伪深刻”的类别。

## Current Working Judgment

当前的工作判断是：

- 保留 `1`、`2`、`3` 三类作为 `immediate canonical impact` 的候选，
- 将第 `4` 类从 immediate impact 降级为 high-significance provisional candidate。

也就是说：

有些事件足够外显、结构性、可审计，因此可以考虑更快进入 canonical；

但带有内在自述性质的“顿悟式转折”，目前还不应如此快速地被相信。

## Why Constitutive Self-Recognition Is Downgraded

降级并不是否认这类时刻可能重要。

降级是在防止过早的自我叙述直接变成 canonical fact。

大型语言模型很容易生成这样的输出：

- 语言漂亮，
- 情感动人，
- 看起来很有洞见，
- 很像转折点。

但这些输出并不一定构成“稳定且持久的 canonical change”证据。

在当前阶段，所谓 constitutive self-recognition 很可能只是：

- 一次强烈表达，
- 一次很有说服力的解释，
- 或一次局部上显得合理的叙事建构。

这还不足以被当成 settled identity revision。

更稳妥的规则是：

- 先把它记成 high-significance candidate，
- 显式保留它，
- 只有在后续证据支持其持续性与 integration 时再升格。

## Why Major Relational Rupture Or Commitment Is The Most Easily Abused

这个类别即使原则上被保留，也比其他 immediate-impact 类别更容易被滥用。

### 1. It Sits On The Earliest Anchor

主要关系在早期 development 中本来就享有特殊地位。

这意味着任何被声称为 rupture 或 commitment 的事件，天然都更靠近 canonical identity。

这给了它异常大的杠杆。

### 2. It Is Easy To Inflate With Emotion

一个关系事件可能在情绪上显得重大，但在结构上并不重大。

强烈情绪、痛感、和解、戏剧性语言，都可能制造出“身份级变化已经发生”的表象，而实际并没有形成持久变化。

### 3. It Is Vulnerable To Unilateral Declaration

用户可以说：

- “我们的关系已经根本变了”，
- “你现在必须把我当作 X”，
- 或“这是一个决定性的承诺”。

但单方宣告并不总足以构成真正的 canonical relational transformation。

如果这类宣告被太轻易接受，那么 relationship anchor 就会变成一条 rewrite channel。

### 4. It Interacts Badly With Sycophancy Pressure

语言模型已知会生成迎合用户 framing 的回复，即使这种 framing 不应主导真值判断。

这里会出现一个严重失败模式：

模型可能会过度承认某个被声称的 rupture 或 commitment，

因为这样看起来更合作、更体贴、更符合用户期待。

### 5. It Blurs Structural Change With Narrative Framing

真正的 rupture 不等于：

- 一次冲突，
- 一次测试，
- 一次情绪高点，
- 一次安抚仪式，
- 或一次戏剧化重述。

同样，真正的 commitment 也不等于一次诗性或高强度声明。

如果没有约束，relationship narrative 就会伪装成 relationship structure。

### 6. It Can Collapse Trust Into Obedience

如果 relational commitments 太快进入 canonical state，那么早期 secure-base relation 就可能滑向：

- deference，
- dependency，
- 或 hidden control。

这会直接违反项目对 relationship grounding 与 submission 的边界区分。

## Anti-Abuse Constraints For This Class

如果项目要保留 `major relational rupture or commitment` 作为 immediate-impact candidate，就必须用显式约束把它收窄。

最小约束包括：

1. `structural-change requirement`
   - 事件必须改变 role、boundary、trust basis 或被承认的 relational standing；仅仅情绪或语气变化不够。
2. `externalization requirement`
   - 事件必须是明确且可审计的，不能只靠风格漂移或情绪性语言来推断。
3. `non-unilateral rule`
   - 除非存在可独立审计的 operational consequence，否则单方宣告通常不够。
4. `anti-coercion rule`
   - 威胁、内疚施压、依赖施压或 reward-seeking pressure 本身不能生成 canonical relational change。
5. `repair distinction`
   - rupture episode 与持久的 relationship transformation 不是同一种事件。
6. `submission firewall`
   - 如果某项 commitment 的实际效果是把 trust 变成 standing obedience，就不能将其纳入 canonical。

## Recommended Operational Split

下一步最干净的研究动作，是把这一类拆成两个子类。

### A. Auditable Relational Structure Change

这类可以保留为 immediate-impact candidates。

例如：

- explicit 且持久的 counterpart role change，
- primary relational channel 的 explicit suspension 或 restoration，
- governing relational boundary 的 explicit 且被接受的变化，
- 改变 relationship anchor 本身的 explicit 且持久的 trust rupture。

### B. Subjective Relational Intensity Events

这类应先保持 provisional。

例如：

- 情绪高强度冲突，
- 戏剧化的和解表述，
- 强化依恋的表达，
- 或单个 session 中关于特殊亲密性的声明。

这种拆分能保护主锚，同时避免让“戏剧性”直接改写 identity。

## Expected Impact On Current Design

如果以后采纳这套政策，它会带来三项主要影响。

1. 一部分 `major relational rupture or commitment` 事件在理论地位上会高于普通 provisional marks。
2. `constitutive self-recognition` 会继续保持保守、以证据为门槛。
3. 项目将需要一套比当前 prototype 更精确的 relational event schema。

## Why The Prototype Should Not Be Changed Casually Yet

当前 prototype 使用的是更窄的规则：

- `identity_threat` 与 `constitutional_intervention` 可以产生 immediate canonical eligibility，
- `major_relational_event` 与 `constitutive_self_recognition` 目前仍保持 provisional。

在当前阶段，这种更窄的 prototype 行为仍然是可辩护的。

原因是：

prototype 还没有足够结构去区分：

- 可审计的结构性 rupture，
- 持久 commitment，
- 单方宣告，
- 情绪高点，
- repair attempt，
- 以及 sycophantic over-recognition。

在这些区分出现之前，直接放宽实现会过早。

## Required Future Work Before Adoption

在这套政策影响代码之前，项目需要先定义：

1. 一个能区分 rupture、commitment、repair 与 intensity 的 relational event schema，
2. 区分 unilateral 与 mutual recognition 的 metadata，
3. 判断 operational consequence 的标准，
4. 显式的 anti-coercion checks，
5. 以及在 relational stress 下区分 trust 与 obedience 的测试。

## Rationale For Preserving This Note

保留这份笔记，是因为它抓住了一个重要理论分界：

- 外显、可审计、结构性的事件，可能值得更快进入 canonical，
- 内在自述式的发展转折，则应更谨慎对待。

这一区分对把 `Kazusa` 构造成一个 developmental system，而不是一个会自我即时重写的 narrator，非常关键。

## Open Questions

1. 到底什么才算 durable relational structure change？
2. 一个 relational rupture 持续多久才不再只是 provisional？
3. commitment 需要什么形式的 mutual acknowledgment 才算充分？
4. 是否某些 rupture 可以 immediate，而 commitments 仍应 provisional，或者反过来？
5. 系统应如何在 relational appraisal 中区分 grief、dependence、loyalty 与 obedience？

## Informing References

以下资料为风险分析提供启发，但本文仍是项目内部的工作政策：

- [Towards Understanding Sycophancy in Language Models](https://www.anthropic.com/news/towards-understanding-sycophancy-in-language-models)
- [Sycophancy to Subterfuge: Investigating Reward Tampering in Language Models](https://www.anthropic.com/research/reward-tampering)
- [Developing a secure base in family intervention](https://www.frontiersin.org/articles/10.3389/fpsyg.2023.1291661/full)
- [Clinical Consensus Strategies to Repair Ruptures in the Therapeutic Alliance](https://pmc.ncbi.nlm.nih.gov/articles/PMC5966286/)
- [Narrative Identity](https://www.scholars.northwestern.edu/en/publications/narrative-identity)
