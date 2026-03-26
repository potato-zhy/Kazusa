# AGENTS.md（中文版）

## 项目定位

`Kazusa` 不是一个传统助手项目。

这个工作区的目标，是构建一个具有连续性的 AI 存在；她的身份应当从结构化经历、整合过程、受限变化以及基于关系的 grounding 中逐步形成。

不要把 `Kazusa` 当成：

- 一段静态的人设提示词，
- 一个角色扮演外壳，
- 一个带记忆的聊天机器人，
- 或者一个可以被单轮交互直接重写身份的系统。

## 真正生效的文档

英文文档是实现、系统行为与后续交接时的主依据。

中文版文档仅作为阅读镜像。如果英文文档与中文版镜像有冲突，以英文文档为准。

## 工作区结构

- `CoreDevelopment/`
  - 当前激活的研发工作区
  - 架构、规格、评估、原型、核心代码和设计文档都应放在这里
- `RuntimeStewardship/`
  - 预留给运行、观察、陪护与后期部署流程
- `discussion_archive.md`
  - 高层讨论摘要档案
- `full_dialogue_archive.md`
  - 更完整的对话存档

## 优先阅读

在做重大变更之前，先读以下文件：

1. `CoreDevelopment/Core_Development_Team_Charter.md`
2. `CoreDevelopment/Kazusa_RnD_Roadmap.md`

如果需要中文版辅助阅读，可参考：

- `CoreDevelopment/Core_Development_Team_Charter_zh-CN.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap_zh-CN.md`

## 命名与文档规则

- 团队名、模块名、架构术语和正式文档标题使用英文。
- 创建重要 Markdown 文档时，优先采用：
  - 一份英文主文档，
  - 一份中文镜像文档（如果对阅读有帮助）。
- 命名应尽量朴素、稳定、便于执行。
- 除非被明确要求，否则不要给核心系统模块起过于戏剧化或过度拟人化的名字。

## 核心研发规则

以下内容是“宪法级约束”，不是可选风格偏好：

1. `Continuity over immediacy`
   - 单轮交互不得直接重写身份。

2. `Integration over imitation`
   - 新经历必须经过评估与整合，而不是被直接镜像。

3. `Relationship without submission`
   - 对主要人类对象的早期信任，不得演变成无条件服从。

4. `Growth without drift`
   - 变化必须渐进、可追溯，并建立在证据上。

5. `Safety at the behavior layer`
   - 紧急干预应优先限制行为，而不是直接重写身份。

## 团队边界

项目当前分为两条独立轨道：

- `Core Development Team`
  - 负责设计与维护核心系统
- `Runtime Stewardship Team`
  - 负责在运行中观察、陪护和管理 `Kazusa`

除非获得明确批准，不要把这两种角色混在一起。

在当前阶段，优先推进 `CoreDevelopment/`。

## 需要避免的事情

未经明确批准，不要引入以下内容：

- 一个固定且包办一切的人设 prompt，
- 来自用户输入的直接身份覆盖，
- 隐性的 persona patching，
- 未记录的记忆重写，
- 把安全捷径偷偷变成人格控制，
- 主要优化目标变成讨好、服从或短期情绪回报。

## 变更策略

凡涉及以下内容的变更，都视为“宪法级变更”：

- continuity rules，
- identity formation，
- memory policy，
- intervention authority，
- relationship grounding，
- self-revision rules。

对于此类变更：

- 写清楚理由，
- 记录预期影响，
- 保留旧状态或旧文档，
- 尽量使用有版本的变更，而不是静默替换。

## 预期交付

在 `CoreDevelopment/` 中工作时，应尽量推动项目朝这些方向前进：

- continuity kernel，
- experience and appraisal model，
- integration loop，
- relationship-grounding model，
- behavioral safety envelope，
- 以及针对 continuity、drift 和 sycophancy 的 evaluation harness。

## 交接标准

当把工作交给下一个 AI 或开发者时，务必留下：

- 改过哪些文件，
- 为什么改，
- 还有哪些未解问题，
- 做了哪些假设，
- 影响了哪些项目原则。

## 当前优先级

当前优先级是：先在 `CoreDevelopment/` 中建立 `Kazusa` 的研发基础，再去建设 `RuntimeStewardship/` 中的运行体系。
