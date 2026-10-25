# Fibber inspection findings

Status: preliminary runtime observations, 2026-10-25.

## Important distinction

The runtime diagnostic exposes at least three layers that must not be conflated:

1. Direct `WeaponPartDefinition.WeaponAttributeEffects` on the barrel part.
2. `Behavior_AttributeEffect` objects referenced by the part's `BehaviorProviderDefinition`.
3. The weapon's displayed stat card and actual in-use behavior.

The stat card is not currently treated as authoritative for the Fibber. The user reports that its displayed stats can be misleading until the weapon is fired. The diagnostics below expose raw data only; they do not establish the exact engine/UI reason for that discrepancy.

## Observed direct barrel modifiers

All entries below were printed as `EModifierType.MT_Scale`. Values are raw exposed constants and should not be interpreted as final percentages without verifying BL2 modifier semantics.

| Barrel | WeaponSpread | WeaponDamage | WeaponReloadSpeed | WeaponFireInterval | WeaponClipSize |
|---|---:|---:|---:|---:|---:|
| Fibber 1 | -1 | -4 | -2 | -5 | +4 |
| Fibber 2 | +3 | +10 | +2 | -5 | +99 |
| Fibber 3 | +10 | -12 | -15 | +20 | +130 |

## Observed behavior-level effects

- Fibber 1 has a behavior effect modifying `WeaponProjectilesPerShot` by +6.
- Fibber 1 also has behavior-level modifiers for spread (+10), fire interval (+10), damage (approximately +3.6), reload speed (+5), and clip size (-3.5).
- Fibber 2 has behavior-level modifiers for spread (-3.5), clip size (-100), fire interval (+5), reload speed (-2), and damage (-9.5).
- Fibber 3 has behavior-level modifiers for clip size (-128), fire interval (-19), spread (-13), reload speed (+14.5), and damage (+13.5).

These modifiers coexist with direct barrel modifiers. Do not assume they simply add together: verify the engine's modifier application, timing, and interaction with other weapon parts.

## Design implications for BL2 Proper Hybrid

- Catalogue part attributes and behavior effects separately.
- Do not use the displayed stat card as the sole source of truth for special weapons.
- Preserve and inspect behavior-provider sequences and their event wiring, not just the effect objects.
- Distinguish static data inspection from runtime tests: actual shot patterns, damage, ammo use, and post-fire stats need controlled in-game verification.
- Avoid mutating shared global objects during early tests. Any future prototype should start with read-only discovery and use a disposable/test save.

## Next validation steps

1. Determine whether the Fibber's relevant effects are attached to the barrel part, weapon definition, projectile definition, or runtime event logic.
2. Inspect the behavior sequence and event/link wiring for the three barrels in a concise format.
3. Record baseline stats and shot behavior in-game for each Fibber variant under controlled conditions.
4. Compare runtime observations with the part data and stat card, and document any discrepancy as an observation rather than an assumed mechanism.
