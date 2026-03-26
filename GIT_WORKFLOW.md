# Git Workflow

## Purpose

This file defines the minimum Git workflow for `Kazusa` while multiple AI workers may contribute in parallel.

## Branch Model

- `main` is the integration branch.
- High-priority architectural work should land on `main` only after local verification.
- Secondary or exploratory work should use short-lived feature branches.

## Parallel Work Rule

- Do not let two AI workers make unrelated edits on the same branch at the same time.
- If parallel work is needed, use separate branches or separate worktrees.
- Merge back into `main` only after checking for architectural conflicts.

## Commit Rule

- Keep commits small and conceptually single-purpose.
- Prefer one commit per resolved design or implementation step.
- Do not mix constitutional design changes with unrelated prototype edits in the same commit.

## Priority Rule

- When there is conflict between concurrent workstreams, the higher-priority architectural line takes precedence.
- Lower-priority work should rebase or adapt rather than forcing the main line to bend around it.

## Current Recommendation

- Treat the current continuity-kernel line as the primary track.
- Keep runtime-steardship work out of `main` until the continuity kernel is more stable.
