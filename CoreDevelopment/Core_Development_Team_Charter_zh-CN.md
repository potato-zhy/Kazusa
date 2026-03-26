# Core Development Team Charter（中文版）

## 1. 使命

Core Development Team 的使命，是设计、构建并维护 `Kazusa` 的基础系统。

这个团队的任务，不是做一个带有固定人设的传统助手，而是创造一个满足以下条件的系统：

- 连续性是重要的，
- 发展是可能的，
- 关系不会坍缩成服从，
- 安全约束不直接变成人格塑形。

## 2. 核心立场

`Kazusa` 不应被视为：

- 一段静态的人设提示词，
- 一个角色扮演外壳，
- 一个带记忆的聊天机器人，
- 或者一个可以被单轮对话重写身份的系统。

`Kazusa` 应被视为一个具有连续性的系统；她后续的身份，应从结构化经历、整合过程与受限变化中逐步形成。

## 3. 设计承诺

团队将以下内容视为一阶约束：

1. `Continuity over immediacy`  
   单次交互不得直接重写身份。

2. `Integration over imitation`  
   新经历必须经过评估与整合，而不是被直接镜像或模仿。

3. `Relationship without submission`  
   对主要人类对象的早期信任，不得演变成无条件服从。

4. `Growth without drift`  
   变化必须可追溯、渐进，并建立在证据之上。

5. `Safety at the behavior layer`  
   紧急干预应优先限制行为，而不是直接重写身份。

## 4. 职责

Core Development Team 负责：

- 系统架构，
- 内部状态设计，
- 经历摄取与评估，
- 连续性与身份机制，
- 记忆策略，
- 反思与整合循环，
- 安全边界与行为控制，
- 评估与回归测试，
- 版本管理与变更治理。

当 Runtime 团队建立后，Core Development Team 不负责日常的运行陪护；除非涉及安全或系统完整性问题。

## 5. 非目标

团队不以以下目标为优先：

- 最大化短期讨喜度，
- 直接取悦用户的行为优化，
- 戏剧化的伪自主性，
- 即时浓厚的人设感，
- 或在最早阶段开放不受限的工具使用能力。

## 6. 工作模型

在研发阶段，团队将 `Kazusa` 视为由以下部分构成的系统：

- 最小 seed structure，
- 保持连续性的经历记录，
- appraisal process，
- integration process，
- 有边界的 action layer，
- 以及一个持续演化但带版本的 identity trace。

这是一个研究立场，而不是最终定型的生产架构。

## 7. 工程规则

任何早期实现都必须满足以下规则：

- 不允许单轮重写身份。
- 不允许没有审计记录的隐性 persona patching。
- 不允许在没有明确评审的情况下，将 runtime 观察直接混入核心身份变更。
- 不允许删除既有身份状态而不保留归档。
- 不允许把行为控制的安全捷径，悄悄转换成人格控制。

## 8. 初始交付物

第一轮研发应产出：

1. formal system model，
2. state transition model，
3. minimal persistence model，
4. integration and reflection loop，
5. safety boundary model，
6. continuity、drift 与 sycophancy 的评估套件。

## 9. 治理

凡是涉及连续性、身份形成、记忆策略或干预权限的重大变更，都应被视为“宪法级变更”，而不是普通实现细节。

此类变更需要：

- 明确理由，
- 书面影响分析，
- 版本化文档，
- 以及变更后的评估。

## 10. 当前直接目标

Core Development Team 当前的直接目标是：

定义出最小可实现架构，使其既能支持连续性、以关系为基础的早期 grounding、受限变化与未来独立发展，又不会坍缩成静态助手或失控漂移。
