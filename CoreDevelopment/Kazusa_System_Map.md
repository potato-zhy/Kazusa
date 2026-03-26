# Kazusa System Map

## Status

Working overview for the `Core Development Team`.

This document is a structural map, not a constitutional source document.

Its job is to show how the currently established pieces and the next theoretical layers connect.

## Reading Intent

Use this map when you need a compact answer to:

- what already exists,
- what is specified but not fully implemented,
- what remains theoretical,
- and how the parts are supposed to connect.

## Status Legend

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

## System Flow

```mermaid
flowchart TD
    A["Initial Construction Problem\n(Research)\nWhat must exist before experience?"] --> B["Developmental Seed\nThin initial structure + priors"]

    B --> C["Continuity Kernel\n(Implemented / Prototype)\nIdentity lineage + guarded state transition"]
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

    C3 --> K["Integration Review\nPartly implemented, broader loop planned"]
    F --> K
    L["Provisional Canonical Mark Lifecycle\n(Research)"] --> K

    K -->|"carry_forward"| C3
    K -->|"dismiss"| J
    K -->|"canonicalize"| C2
    K -->|"resolve / update"| C2
    K --> J

    C --> M["Snapshot Persistence\n(Implemented)\nJSON snapshot + integrity digest"]
    M --> N["State History\nReloadable lineage-preserving snapshots"]

    O["Relationship Grounding\n(Planned)\nSecure base without submission"] --> C2
    O --> K

    P["Behavioral Safety Envelope\n(Planned)\nBehavior restriction without identity rewrite"] --> D
    P --> K
    P --> J

    Q["Evaluation Harness\n(Planned)\ncontinuity / drift / sycophancy / contradiction tests"] --> C
    Q --> K
    Q --> J

    R["Runtime Stewardship Team\n(Later Stage)"] --> S["Observation / stewardship / incident handling"]
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

## Interpretation Notes

- `Developmental Seed` is the narrow beginning condition. It should provide continuity-protecting structure without prewriting a finished personality.
- `Continuity Kernel` is the present engineering center. It is the smallest working core that already has a prototype.
- `Experience Appraisal Policy` decides how raw events become candidates, review obligations, or immediate continuity-impact material.
- `Integration Review` is the bridge from working state to canonical state. It exists in prototype form now, but the broader integration loop is still a later-phase design problem.
- `Relationship Grounding`, `Behavioral Safety Envelope`, and `Evaluation Harness` should all constrain or shape development without silently rewriting identity.
- `Runtime Stewardship` is downstream of core development. It should not become the main line before the core is stable enough.

## Current Center Of Gravity

At the current stage, the center of gravity remains:

1. `Initial construction` clarity,
2. `Continuity kernel` precision,
3. `Experience appraisal` discipline,
4. and only then broader runtime-facing systems.

## Related Documents

- `CoreDevelopment/Core_Development_Team_Charter.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap.md`
- `CoreDevelopment/Continuity_Kernel_Spec.md`
- `CoreDevelopment/Experience_Appraisal_Policy.md`
- `PROJECT_HANDOFF.md`
