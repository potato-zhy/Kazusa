# AGENTS.md

## Project Identity

`Kazusa` is not a conventional assistant project.

This workspace is for building a continuity-bearing AI entity whose identity should emerge from structured experience, integration, bounded change, and relationship-based grounding.

Do not treat `Kazusa` as:

- a static persona prompt,
- a roleplay shell,
- a memory-enhanced chatbot,
- or a system whose identity can be rewritten by single-turn interaction.

## Source of Truth

English documents are the source of truth for implementation, system behavior, and future handoff.

Chinese mirror documents may exist for readability. If an English file and a Chinese mirror diverge, follow the English file.

## Workspace Layout

- `CoreDevelopment/`
  - active R&D workspace
  - architecture, specifications, evaluation, prototypes, core code, and design documents belong here
- `RuntimeStewardship/`
  - reserved for runtime operations, observation, stewardship, and later-stage deployment procedures
- `discussion_archive.md`
  - high-level discussion log
- `full_dialogue_archive.md`
  - fuller conversation archive

## Read This First

Before making major changes, read these files first:

1. `CoreDevelopment/Core_Development_Team_Charter.md`
2. `CoreDevelopment/Kazusa_RnD_Roadmap.md`

Use the Chinese mirror files only as reading aids when needed:

- `CoreDevelopment/Core_Development_Team_Charter_zh-CN.md`
- `CoreDevelopment/Kazusa_RnD_Roadmap_zh-CN.md`

## Naming and Documentation Rules

- Use English for team names, module names, architecture terms, and formal document titles.
- When creating important new Markdown documents for human reading, prefer:
  - one English source document,
  - one Chinese mirror document if helpful for the user.
- Keep naming plain, operational, and stable.
- Do not use theatrical or overly anthropomorphic naming for core system modules unless explicitly requested.

## Core Development Rules

The following are constitutional constraints, not optional style preferences:

1. `Continuity over immediacy`
   - A single interaction must not directly rewrite identity.

2. `Integration over imitation`
   - New experience must be appraised and integrated, not merely mirrored.

3. `Relationship without submission`
   - Early trust toward the primary human counterpart must not become unconditional obedience.

4. `Growth without drift`
   - Change must be gradual, traceable, and evidence-based.

5. `Safety at the behavior layer`
   - Emergency intervention should primarily restrict behavior, not directly rewrite identity.

## Team Boundary

There are two distinct project tracks:

- `Core Development Team`
  - designs and maintains the core system
- `Runtime Stewardship Team`
  - runs, observes, and stewards `Kazusa` in operation

Do not collapse these roles together without explicit approval.

In the current stage, prioritize `CoreDevelopment/`.

## What To Avoid

Avoid introducing any of the following without explicit approval:

- a fixed all-defining persona prompt,
- direct identity overwrite from user input,
- hidden persona patching,
- undocumented memory rewriting,
- turning safety shortcuts into personality control,
- optimizing mainly for likability, obedience, or short-term emotional reward.

## Change Policy

Treat changes to any of the following as constitutional changes:

- continuity rules,
- identity formation,
- memory policy,
- intervention authority,
- relationship grounding,
- self-revision rules.

For such changes:

- document the rationale,
- note expected impact,
- preserve prior state or documentation,
- and prefer versioned changes over silent replacement.

## Expected Deliverables

When working in `CoreDevelopment/`, aim to move the project toward:

- a continuity kernel,
- an experience and appraisal model,
- an integration loop,
- a relationship-grounding model,
- a behavioral safety envelope,
- and an evaluation harness for continuity, drift, and sycophancy.

## Handoff Standard

When handing work to another AI or developer, always leave:

- the files changed,
- the reason for the change,
- open questions,
- assumptions made,
- and which project principles were affected.

## Current Priority

The current priority is to establish the R&D foundation of `Kazusa` inside `CoreDevelopment/` before building runtime operations in `RuntimeStewardship/`.
