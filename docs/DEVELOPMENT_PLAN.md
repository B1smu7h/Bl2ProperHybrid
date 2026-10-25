# Development Plan

## Phase 0 — Local environment verification

Goal: establish a reproducible baseline before any gameplay mutation.

### User environment (reported)

- Vanilla Borderlands 2.
- Running on Linux through Proton GE.
- Standby level 80 Salvador save available for testing.
- Exact storefront, game build, DLC coverage, and currently installed SDK/mod-loader state are not yet confirmed.

### Safety requirements

- Create a separate copy of the Salvador save before any test.
- Keep the game vanilla until the diagnostic SDK loader is confirmed.
- Do not test part-list or save-validation behavior on the only copy of a valuable character.
- Keep diagnostic logs and note the exact test steps and game session.

### Checklist

- [ ] Confirm Steam or Epic version.
- [ ] Confirm whether all official DLC is installed.
- [ ] Confirm current Proton GE version.
- [ ] Confirm whether an SDK/mod loader is already installed, and where.
- [ ] Back up the test save to a separate location.
- [ ] Confirm the current recommended UnrealSDK / pyunrealsdk installation procedure for BL2 under Proton.
- [ ] Launch with a minimal diagnostic mod and capture its startup log.
- [ ] Verify that a diagnostic script can inspect a known object without altering gameplay.

## Phase 1 — Runtime reconnaissance

- Discover useful weapon-definition and part-list objects.
- Identify candidate functions related to item generation, part selection, item-card presentation, and save/load restoration.
- Record evidence and confidence for each discovery.
- Do not hook production loot generation until the candidate function and call timing are understood.

## Phase 2 — Research catalogue

Start with 6–10 unique weapons that represent different implementation categories:
- Mostly static-stat unique.
- Unusual projectile pattern.
- Unusual firing mode.
- Reload/ammo behavior.
- Conditional or proc-based effect.
- A case where the red text may be mostly flavor.

For each entry, record the definition object, unique parts, effect category, likely implementation, transfer hypothesis, conflicts, presentation source, save/load risk, and evidence level.

## Phase 3 — Proof of concept

- Pick two same-class unique weapons with reasonably understood, part-based effects.
- Test a data-only part-pool approach first where safe.
- If necessary, test a runtime hook after verifying it.
- Confirm both behaviors in combat.
- Confirm the item remains valid after inventory changes and save/quit/reload.
- Record test results in the catalogue.

## Phase 4 — General hybrid framework

Only after the proof of concept:
- Create a data-driven effect catalogue and reusable adapter registry.
- Add configurable chance, donor pools, exclusions, and effect-count rules.
- Define how effects compose and conflict.
- Implement persistent hybrid identity and item-card presentation.
- Add diagnostics for skipped/unsupported combinations.
- Test compatibility and co-op separately.

## Architecture principle

Avoid a hardcoded host/donor pair matrix. Use reusable effect records/adapters. Some individual effect types may require adapters; that is compatible with a data-driven framework. Do not assume every unique mechanic can be transferred identically.

## Decision gates

1. SDK loads and can inspect objects reliably.
2. One hybrid generates and survives save/load.
3. A structurally different effect can be added via a reusable adapter.
4. Multiple effects can be composed without bespoke code per pair.
