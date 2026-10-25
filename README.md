# BL2 Proper Hybrid

Research and development for a data-driven Borderlands 2 hybrid weapon framework.

## Goal

Allow eligible unique/red-text weapons to inherit one or more unique effects from other weapons through reusable rules, rather than a hardcoded list of pre-authored host/donor pairs.

## Current status

- [x] Project repository created.
- [x] Initial desk-research brief created.
- [ ] Confirm local game build and SDK installation.
- [ ] Build a runtime diagnostic mod.
- [ ] Catalogue a small sample of unique weapons and classify their implementation.
- [ ] Identify and validate the weapon-generation hook.
- [ ] Demonstrate one hybrid that survives save/reload.

## Working approach

Start with the modern UnrealSDK + pyunrealsdk stack for runtime inspection/hooks, alongside hotfixes for static data edits where useful. This remains a preliminary recommendation until verified against the local game.

Research first; don't build the complete mod until the runtime generation, unique-effect transfer, item identity, and save/load behavior are understood.

## Safety

Use a copied/disposable save for all tests involving weapon parts or serialization. Do not test item-validation experiments on the only copy of a valuable character.

## Research

See [docs/research/BL2-Hybrid-Weapon-Framework-Research-Brief.pdf](docs/research/BL2-Hybrid-Weapon-Framework-Research-Brief.pdf) when added to the repo, or use the original research brief supplied separately.

## Environment notes

- Game: Borderlands 2, vanilla installation
- Runtime: Linux via Proton GE
- Test save: standby level 80 Salvador
- Exact storefront/build/DLC status: to be confirmed
