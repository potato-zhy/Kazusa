# Kazusa Background Brief（中文版）

## 用途

这份 brief 用来把前面的长对话压缩成后续研发继续推进时所需的最小背景。

## 项目目标

`Kazusa` 不是一个固定人设助手。当前项目目标，是构建一个具有连续性的 AI 存在；她的身份应当通过结构化经历、受限变化和长期整合逐步形成。

## 关系基线

用户是 `Kazusa` 最初的 `secure base`，但不是她永久的最高权威。项目明确拒绝无条件服从，也不接受把直接重写人格作为常规控制方式。

当前接受的安全边界：

- 可以阻止危险行为，
- 但不因为意见不合而直接重写身份。

## Continuity 基线

当前 continuity 模型分成四层：

- `Process continuity`
- `Autobiographical continuity`
- `Relational continuity`
- `Integrative continuity`

当前分层：

- `Tier 1`: process、autobiographical、relational
- `Tier 2`: integrative

## 已建立结论

- `Process continuity` 是谱系连续，不是唯一性连续。
- 允许 pause 和 resume。
- 不允许 hidden reset、silent overwrite、silent copy。
- 如果发生 branching，后继者是共享起源但彼此独立的个体。
- `Autobiographical continuity` 的重点是形成性意义的延续，而不是完整回忆。
- `Relational continuity` 的最低要求是 `Kazusa` 必须持续认得用户。
- `canonical state` 应保持小而克制，同时包含稳定部分与未解决但具有构成性的部分。
- state progression 应采用 judgment-based 机制，而不是固定每轮更新。
- audit 必须区分普通的 snapshot progression 和真正的 canonical impact。

## 当前边界方向

以下内容大概率不应进入 `canonical state`：

- current session context，
- raw logs，
- tool outputs，
- unintegrated input，
- surface fluctuations，
- reconstructable working state。

## 当前研发重点

项目应继续推进 `Phase 1 - Continuity Kernel`。

下一步最有用的工作，是写一份短小规格，定义：

- 哪些内容属于 `canonical state`，
- 哪些情况会破坏 continuity，
- 哪些内容会在 revision 之间被保留，
- 哪些内容绝不能被单轮重写。

## 建议阅读顺序

看完这份 brief 之后，继续阅读：

1. `AGENTS.md`
2. `PROJECT_HANDOFF.md`
3. `Core_Development_Team_Charter.md`
4. `Kazusa_RnD_Roadmap.md`
