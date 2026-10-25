"""Compact read-only BL2 behavior-provider report for Fibber and Evil Smasher.

Run from the BL2 SDK Python console:
    pyexec scripts/fibber_wiring_v3.py

This version calls the SDK provider getter when available, deduplicates providers,
and prints only event names, behavior object paths, skill references, and nested
attribute-effect values. It does not modify game state.
"""

import unrealsdk

TOKENS = ("fibber", "evilsmash")
MAX_ITEMS = 32


def get(obj, name):
    try:
        return getattr(obj, name)
    except Exception:
        return None


def path(obj):
    if obj is None:
        return "<none>"
    for name in ("PathName", "FullName", "Name"):
        value = get(obj, name)
        if value is not None:
            try:
                value = value() if callable(value) else value
                return str(value)
            except Exception:
                pass
    return str(obj)


def items(value):
    if value is None:
        return []
    try:
        return list(value)
    except Exception:
        return []


def provider_for(part):
    # In this SDK, BehaviorProviderDefinition may be a getter/setter-backed
    # interface rather than a directly readable property.
    getter = get(part, "GetBehaviorProviderDefinition")
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return value
        except Exception:
            pass
    value = get(part, "BehaviorProviderDefinition")
    return value


def name_of(value):
    if value is None:
        return "<none>"
    for field in ("EventName", "SequenceName", "Name"):
        candidate = get(value, field)
        if candidate is not None:
            return str(candidate)
    return path(value)


def print_attribute_effects(behavior, indent="        "):
    # Attribute effects may be nested under Behavior_AttributeEffect.Behavior.
    nested = get(behavior, "Behavior")
    candidates = [behavior]
    if nested is not None:
        candidates.append(nested)

    for candidate in candidates:
        effects = items(get(candidate, "AttributeEffects"))
        for i, effect in enumerate(effects[:MAX_ITEMS]):
            attr = get(effect, "AttributeToModify")
            modtype = get(effect, "ModifierType")
            base = get(effect, "BaseModifierValue")
            constant = get(base, "BaseValueConstant") if base is not None else None
            print(
                f"{indent}ATTR[{i}] attribute={path(attr)} "
                f"modifier={modtype} base_constant={constant}"
            )


print("=== BL2 Fibber/Evil Smasher compact wiring report (READ ONLY) ===")

try:
    parts = list(unrealsdk.find_all("WeaponPartDefinition"))
except Exception as exc:
    print("Could not enumerate WeaponPartDefinition:", repr(exc))
    raise

matches = [p for p in parts if any(t in path(p).lower() for t in TOKENS)]
print(f"WeaponPartDefinition objects: {len(parts)}; matching parts: {len(matches)}")

seen = set()
for part in matches:
    part_path = path(part)
    provider = provider_for(part)
    print(f"\nPART {part_path}")
    print(f"  provider: {path(provider)}")

    if provider is None:
        related = []
        try:
            related = [
                n for n in dir(part)
                if "behavior" in n.lower() or "provider" in n.lower()
            ]
        except Exception:
            pass
        print(f"  provider getter unavailable; related names: {related[:20]}")
        continue

    provider_path = path(provider)
    if provider_path in seen:
        print("  provider already summarized")
        continue
    seen.add(provider_path)

    sequences = get(provider, "BehaviorSequences")
    if sequences is None:
        sequences = get(provider, "Sequences")
    seqs = items(sequences)
    print(f"  sequences: {len(seqs)}")

    for si, seq in enumerate(seqs[:MAX_ITEMS]):
        print(
            f"  SEQ[{si}] name={name_of(seq)} "
            f"enabled_on_spawn={get(seq, 'bEnabledOnSpawn')}"
        )

        events = items(get(seq, "EventData2"))
        for ei, event in enumerate(events[:MAX_ITEMS]):
            user_data = get(event, "UserData")
            event_name = get(user_data, "EventName") if user_data is not None else None
            enabled = get(user_data, "bEnabled") if user_data is not None else None
            print(f"    EVENT[{ei}] name={event_name} enabled={enabled}")

        behaviors = items(get(seq, "BehaviorData2"))
        for bi, item in enumerate(behaviors[:MAX_ITEMS]):
            behavior = get(item, "Behavior")
            print(f"    BEHAVIOR[{bi}] item={path(item)}")
            print(f"      behavior={path(behavior)}")

            for field in ("SkillToActivate", "SkillToDeactivate"):
                skill = get(behavior, field) if behavior is not None else None
                if skill is not None:
                    print(f"      {field}={path(skill)}")

            print_attribute_effects(behavior)

print("\n=== End compact report; no game state was changed ===")
