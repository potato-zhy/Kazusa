# Kazusa System Map（中文镜像）

## 状态

这是给 `Core Development Team` 使用的工作总览图。

它不是宪法级源文档。

它的作用是把当前已经建立的部分、已写明但未完全实现的部分、以及接下来理论上要落地的部分，用结构关系图串起来。

## 阅读目的

当你需要快速回答下面这些问题时，可以先看这份图：

- 现在已经有什么，
- 哪些已经写成规范但还没完全实现，
- 哪些仍在理论阶段，
- 它们彼此之间怎么连接。

## 状态图例

- `Implemented / Prototype`
  - continuity kernel prototype
  - JSON snapshot persistence
  - continuity-kernel tests
- `Specified`
  - continuity kernel specification
  - experience appraisal policy
  - mark review outcomes
- `Research / In Progress`
  - initial construction problem
  - immediate canonical impact boundary
  - provisional canonical mark lifecycle
- `Planned`
  - integration loop
  - relationship grounding
  - behavioral safety envelope
  - evaluation harness
  - runtime stewardship handoff

## 系统流程图

```mermaid
flowchart TD
    A["Initial Construction Problem\n(Research)\n在经验累积前必须先有什么？"] --> B["Developmental Seed\n薄初始结构 + priors"]

    B --> C["Continuity Kernel\n(Implemented / Prototype)\n身份谱系 + 受保护的状态迁移"]
    C --> C1["Lineage Layer\nentity_id / branch_id / parent_state_id / state_version"]
    C --> C2["Canonical State Layer\nconstitutional commitments\nrelationship anchor\nself-model summary\nautobiographical signals\nopen tensions"]
    C --> C3["Working State Layer\nevent_log\nprovisional_signals\nprovisional_canonical_marks\naudit_log"]

    D["Incoming Experience\nuser / system / world / tool-related events"] --> E["Event Ingestion"]
    F["Experience Appraisal Policy\n(Specified)"] --> E
    G["Immediate Canonical Impact Boundary\n(Research)"] --> E

    E --> C3
    E --> H{"Handling Level"}
    H -->|"Logged only"| C3
    H -->|"Provisional signal"| C3
    H -->|"Provisional canonical mark"| C3
    H -->|"Immediate canonical eligibility"| I["Immediate audited canonical impact"]

    I --> C2
    I --> J["Audit Trace"]

    C3 --> K["Integration Review\n已有原型，完整 integration loop 仍待后续扩展"]
    F --> K
    L["Provisional Canonical Mark Lifecycle\n(Research)"] --> K

    K -->|"carry_forward"| C3
    K -->|"dismiss"| J
    K -->|"canonicalize"| C2
    K -->|"resolve / update"| C2
    K --> J

    C --> M["Snapshot Persistence\n(Implemented)\nJSON snapshot + integrity digest"]
    M --> N["State History\n可重载、保留 lineage 的快照历史"]

    O["Relationship Grounding\n(Planned)\nsecure base 但不坍缩为 submission"] --> C2
    O --> K

    P["Behavioral Safety Envelope\n(Planned)\n限制行为，而不是重写身份"] --> D
    P --> K
    P --> J

    Q["Evaluation Harness\n(Planned)\ncontinuity / drift / sycophancy / contradiction tests"] --> C
    Q --> K
    Q --> J

    R["Runtime Stewardship Team\n(后续阶段)"] --> S["observation / stewardship / incident handling"]
    C --> R
    O --> R
    P --> R
    Q --> R

    classDef proto fill:#d9f2ff,stroke:#1d70b8,color:#000;
    classDef spec fill:#e8f5e9,stroke:#2e7d32,color:#000;
    classDef research fill:#fff3e0,stroke:#ef6c00,color:#000;
    classDef planned fill:#f3e5f5,stroke:#7b1fa2,color:#000;

    class C,C1,C2,C3,M,N proto;
    class F spec;
    class A,G,L research;
    class O,P,Q,R,S planned;
```

## 解读说明

- `Developmental Seed` 是最窄的起始条件。它提供保护连续性的结构，但不预写一个完成的人格。
- `Continuity Kernel` 是当前最核心的工程中心，也是现在已经有 prototype 的地方。
- `Experience Appraisal Policy` 负责决定原始事件如何变成候选、复核义务、或即时连续性影响材料。
- `Integration Review` 是从 working state 通往 canonical state 的桥。它现在已有原型，但更完整的 integration loop 仍属于后续阶段。
- `Relationship Grounding`、`Behavioral Safety Envelope`、`Evaluation Harness` 都应当影响发展过程，但不能静默重写身份。
- `Runtime Stewardship` 是核心研发之后的下游部分，在 core 足够稳定之前，不应反过来成为主线。

## 当前重心

当前阶段的重心仍然是：

1. `Initial construction` 的清晰化，
2. `Continuity kernel` 的精确化，
3. `Experience appraisal` 的纪律化，
4. 然后才是更广泛的 runtime-facing 系统。

## 相关文档

- `CoreDevelopment/Core_Development_Team_Charter.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap.md`
- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Experience_Appraisal_Policy.md`
- `PROJECT_HANDOFF.md`
