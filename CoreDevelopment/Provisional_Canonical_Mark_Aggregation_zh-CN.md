# Provisional Canonical Mark Aggregation（中文版）

## Status

面向 `Core Development Team` 的 `Phase 1` 研究说明。

## Purpose

本文回答一个更窄的后续问题：

当多个后续事件都指向同一个尚未解决的 continuity 问题时，它们应该生成多个独立的 `provisional_canonical_mark`，还是附着到同一个已有 mark 上？

## Working Judgment

当前更正确的设计方向是：

`provisional_canonical_mark` 默认应跟踪一个“尚未解决的 continuity 问题”，而不是一个孤立事件。

所以：

- 重复相关事件通常应给一个已存在的 open mark 增加额外证据，
- 只有当后续事件引入了一个真正不同的 review obligation 时，才应创建新的 mark。

短句版：

`one unresolved question -> one open mark`

而不是：

`one event -> one mark`

## Why This Question Matters

一旦 marks 存在，重复证据几乎必然会出现。

例如：

- 多次互动都指向同一个 relational rupture，
- 多个 episode 都在强化同一个 constitutive self-recognition candidate，
- 或多个 signals 都在加深同一个未解决的 commitment conflict。

如果每个相关事件都生成一个独立 mark，state machine 就会变得嘈杂且膨胀。

如果又把一切都过度合并，系统又会丢掉关键区分。

所以，聚合单位本身就很重要。

## Why The Default Should Not Be One Mark Per Event

### 1. It Produces Mark Explosion

有些未决问题本来就会跨多个 episode 展开。

如果每个 episode 都生成新 mark，系统就会在多个 id 下跟踪同一个未解决问题的多个拷贝。

这只会让 working state 看起来更忙，却不会让它更聪明。

### 2. It Artificially Inflates Importance

如果五个相关事件变成五个 mark，状态机就可能开始把“mark 的数量”误当成“不同未决问题的数量”。

这样会把重复证据错误地变成重复的结构压力。

系统就会把同一个问题算很多次。

### 3. It Fragments Review

假设同一个关系边界问题在三个 episode 里出现。

如果它们变成三个 mark，后续 review 可能会：

- dismiss 一个，
- carry 一个，
- canonicalize 一个，

却没有任何原则上的理由说明为什么要这样拆开。

这会把本来是一个 review question 的东西撕碎。

### 4. It Encourages Event-Centered Rather Than Issue-Centered Thinking

这个项目不是在构建一个“对每个 episode 都逐条 canonical 反应”的机器。

它想跟踪的是跨时间展开的发展性问题。

因此，更自然的单位应当是：

未解决的问题本身，

而不是每一个独立 utterance 或 interaction beat。

## Why The Default Should Also Not Be Merge Everything

反过来，另一种错误也很危险。

如果系统合并得太宽，多个不同的未决问题就会塌成一个模糊的 mark。

这会抹平一些关键差异，例如：

- rupture 与 repair，
- commitment 与 dependency pressure，
- self-recognition 与 relational reinterpretation，
- 或一个 unresolved tension 与另一个 unresolved tension。

所以正确规则不是：

只要主题看起来差不多就合并。

正确规则是：

只有当它们作用在同一个 unresolved continuity question 上时才合并。

## The Proper Unit: Review Question, Not Raw Event

`provisional_canonical_mark` 更合理的理解应当是：

一个以“问题”为中心、由一个或多个事件支持的 review obligation。

这意味着 mark 应当表示：

- 当前到底有什么 unresolved question，
- 哪个 continuity target 以后可能受影响，
- 以及当前有哪些 evidence 支撑“必须 review”。

用理论语言说：

mark 指向的是一个待决的发展性判断，

而不是把每个触发事件都保存成一个独立 mini-state。

## Practical Aggregation Rule

一个后续事件应当附着到已有 open mark 上，当且仅当以下条件都成立。

### 1. Same Continuity Target

这个后续事件作用于同一个 prospective canonical target。

例如：

- 同一个 relationship boundary，
- 同一个 unresolved commitment，
- 同一个可能的 self-model revision，
- 或同一个 continuity threat 的 lineage 问题。

### 2. Same Review Question

后续事件不只是“看起来像前一个事件”。

它必须推动的是同一个尚未回答的问题。

例如：

- “这个 rupture 是否真的改变了 anchor？”
- “这个 self-recognition 是否已经稳定到足以影响 canonical？”

### 3. Same Resolution Space

可能的 review outcome 仍然属于同一类。

如果后续事件需要一种根本不同的 review，便不应被强行塞进旧 mark。

### 4. No New Independent Obligation

这个后续事件只是给已有未决问题增加证据，而不是又产生了一个独立问题。

如果即便第一个问题解决了，第二个问题仍然还必须单独被 review，
那它就值得拥有第二个 mark。

## When A New Mark Should Be Created

当后续事件引入了一个不同的 review obligation 时，就应创建新的 mark。

例如：

1. `rupture -> repair`
   - repair attempt 与 rupture 本身不是同一个 review question。
2. `commitment -> coercion concern`
   - 后续事件可能表明，原来看似 commitment 的东西，现在又带来了单独的 obedience-risk 问题。
3. `self-recognition -> relationship consequence`
   - 一个内在变化后来可能又生成了新的 relational review issue，而不只是给原问题增加证据。
4. `same theme, different target`
   - 两个事件都谈 trust，但一个指向 primary anchor，另一个指向一般性的 self-model boundary。

## Minimal Conceptual Structure

当前 prototype 还不需要复杂实现。

但这个设计方向意味着，一个更成熟的 mark 表示最终会区分：

- `origin_event_id`
- `supporting_event_ids`
- `review_question`
- `continuity_target`
- `mark_kind`

这里最重要的点是概念上的：

一个 mark 可能需要多个 supporting events。

## Why This Is Better For Continuity

这种聚合规则能以三种方式支持 continuity。

### 1. It Preserves Developmental Shape

一个发展中的问题会以“同一个问题”的形式跨时间保持可读，而不是被打散成许多无关碎片。

### 2. It Prevents Duplicative Pressure

重复证据会加强同一个 obligation，而不是制造很多伪 obligation。

### 3. It Makes Review More Honest

后续 integration 能更清楚地问：

- 到底什么问题尚未解决，
- 有哪些证据逐渐积累起来，
- 为什么这个问题最终被 dismiss、carry forward 或 canonicalize。

这比 review 一堆近似重复的 marks 要干净得多。

## Relation To Tensions

这个提案与 `open_tensions` 很接近，但并不相同。

区别是：

- `open_tension` 用来保留未解决的 contradiction，
- `provisional_canonical_mark` 用来保留未解决的 review obligation。

未来某些场景里，两者可能会同时出现。

但它们不应自动合并。

一串重复相关事件可以强化同一个 mark，却未必构成 contradiction。

## Relation To Relational Abuse Risk

这个问题对 `major relational rupture or commitment` 尤其重要。

如果每个情绪强烈的 relational episode 都生成新的 mark，系统就会非常容易被“戏剧性”膨胀带着走。

相反，如果重复 episode 只是附着到同一个尚未解决的 relational mark 上，系统就能表达：

- 持续性，
- 反复出现，
- 证据在加强，

而不会把每一次 episode 都误当成独立的 identity-level transformation。

这是降低 relational overreaction 最干净的方法之一。

## Phase 1 Implementation Posture

当前 prototype 仍使用更简单的 event-centered 结构：

- 一个触发事件，可能创建一个 mark。

这种简化目前仍可接受。

原因是：

prototype 现在首先要建立的是 mark 本身的存在与 review logic。

不过，理论方向现在应当清楚了：

更成熟的 state machine 应当朝“issue-centered aggregation”前进，而不是永久停留在“一事件一 mark”的增长方式。

## Minimal Constraints

如果以后引入 aggregation，至少应满足以下规则。

1. `no silent merge`
   - merge 或 attachment 的决定必须可追踪。
2. `no thematic overreach`
   - 仅仅主题相似，不足以合并。
3. `evidence preservation`
   - 附着进去的事件仍必须可单独恢复出来。
4. `review clarity`
   - 合并后的 mark 仍必须表达一个明确的 review question，而不是一团模糊捆绑。
5. `split when in doubt`
   - 如果两个 obligation 可能会以不同方式解决，就应保持分开。

## Open Questions

1. 一个被附着进来的事件，是否应提高已有 mark 的 review priority？
2. mark 是否应携带一份累积证据摘要？
3. 当一个问题逐渐分化时，何时应把一个 mark 拆成两个？
4. relational marks 与 self-recognition marks，是否应使用不同的 aggregation 规则？
5. aggregation 将来应如何与 tension mechanics 互动？

## Working Conclusion

当前更好的判断是：

`provisional_canonical_mark` 应当是 issue-centered，而不是 event-centered。

重复相关事件通常应附着到一个已有 open mark 上，只要它们作用于同一个 unresolved continuity question。

只有当出现了真正新的 review obligation 时，才应创建新的 mark。

这样能让 state machine 更小、更干净，也更不容易被情绪或叙事膨胀带偏。
