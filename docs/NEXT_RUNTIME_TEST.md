# Next runtime test: behavior sequence wiring

Goal: understand when Fibber and Evil Smasher behavior effects execute before attempting any hybrid mutation.

## Safety and setup

- Keep this pass read-only. Do not change weapon parts, behavior objects, skill definitions, or hotfixes.
- Use the existing level-80 Salvador test character and a disposable copy of the save if possible.
- Record which weapon variant is being inspected and avoid changing several variables at once.
- The previous diagnostics completed without changing game state.

## Test A — Fibber baseline observations

For each of the three Fibber barrel variants, record:

1. The exact weapon/variant and visible stat-card values before firing.
2. Magazine size and reserve ammo.
3. A short controlled firing test at a stationary target, noting projectile pattern, number of visible projectiles, ammo consumed per trigger pull, and any unusual impacts.
4. Reload behavior and the stat card immediately afterward.
5. Whether the behavior changes after swapping away and back to the weapon.

Keep distance, target, character, skills, class mods, relics, and other gear constant. Do not infer exact damage from floating numbers unless the test setup controls for critical hits, resistances, and other bonuses.

## Test B — inspect behavior wiring

Run the next behavior-sequence diagnostic script once it is provided. It should report, for each Fibber barrel and the Evil Smasher barrel:

- sequence index/name and enabled-on-spawn flag;
- event names and enabled flags;
- output links and output variables;
- behavior object class, full object path, and relevant target references;
- for behavior effects, the attribute name and modifier value where exposed;
- for activation/deactivation behaviors, the referenced skill definition.

The output should be compact and should not recursively print entire Unreal objects.

## Test C — Evil Smasher event observations

Before testing, record the current equipped weapon and magazine state. Then observe separately:

1. Equip Evil Smasher.
2. Fire without reloading.
3. Reload once and observe whether a buff occurs.
4. Repeat reloads enough times to notice the chance-based nature, without assuming a small sample proves the exact probability.
5. Swap away and back, noting whether any buff or state persists.

Do not combine this with Fibber tests. The diagnostic is intended to identify event wiring; in-game observations are intended to establish actual behavior.

## Conference Call — later comparison case

After the first two cases, inspect Conference Call as a projectile/spread behavior case. Use the same read-only approach to identify its projectile definitions and behavior wiring, then compare its firing pattern against its data. It is a useful contrasting case, but not required to complete the first diagnostic milestone.

## Report back

Send the compact diagnostic output and concise observations. Screenshots are fine if the console output is too large. No need to send a full log unless the script reports an exception.
