"""Read-only discovery of Fibber/Evil Smasher weapon parts and behavior providers.

Run in the BL2 SDK Python console:
    pyexec scripts/fibber_wiring.py

This pass first finds weapon parts by path, then follows their exposed
BehaviorProviderDefinition reference. It does not modify game state.
"""

import unrealsdk

TOKENS = ("fibber", "evilsmash")
MAX_ITEMS = 24


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


def as_list(value):
    if value is None:
        return []
    try:
        return list(value)
    except Exception:
        return []


def show_fields(obj, names, indent="      "):
    for name in names:
        value = get(obj, name)
        if value is not None:
            print(f"{indent}{name}: {path(value)}")


print("=== BL2 Fibber/Evil Smasher provider discovery (READ ONLY) ===")

try:
    parts = list(unrealsdk.find_all("WeaponPartDefinition"))
    print("WeaponPartDefinition objects enumerated:", len(parts))
except Exception as exc:
    print("Could not enumerate WeaponPartDefinition:", repr(exc))
    raise

matches = [p for p in parts if any(t in path(p).lower() for t in TOKENS)]
print("Matching weapon parts:", len(matches))

seen_providers = set()
for part in matches:
    print("\nPART:", path(part))
    show_fields(part, (
        "BehaviorProviderDefinition",
        "WeaponAttributeEffects",
        "WeaponProjectiles",
        "ProjectileDefinition",
    ), "  ")

    provider = get(part, "BehaviorProviderDefinition")
    if provider is None:
        print("  No BehaviorProviderDefinition property exposed under that name.")
        try:
            names = [n for n in dir(part) if "behavior" in n.lower() or "provider" in n.lower()]
            print("  Related exposed names:", names[:40])
        except Exception:
            pass
        continue

    provider_path = path(provider)
    if provider_path in seen_providers:
        print("  Provider already printed:", provider_path)
        continue
    seen_providers.add(provider_path)

    print("  PROVIDER:", provider_path)
    sequences = get(provider, "BehaviorSequences")
    if sequences is None:
        sequences = get(provider, "Sequences")
    seqs = as_list(sequences)
    print("  Sequence collection:", "exposed" if sequences is not None else "not exposed",
          f"({len(seqs)} entries)")

    for si, seq in enumerate(seqs[:MAX_ITEMS]):
        print(f"    SEQUENCE [{si}]: {path(seq)}")
        show_fields(seq, (
            "SequenceName", "Name", "bEnabledOnSpawn", "EnabledOnSpawn"
        ), "      ")

        for field in ("EventData2", "BehaviorData2"):
            entries = as_list(get(seq, field))
            print(f"      {field}: {len(entries)} entries")
            for i, entry in enumerate(entries[:MAX_ITEMS]):
                print(f"        [{i}] {path(entry)}")
                show_fields(entry, (
                    "Event", "EventName", "Name", "bEnabled", "Enabled",
                    "Behavior", "BehaviorSequence", "SkillToActivate",
                    "SkillToDeactivate", "OutputLinks", "OutputVariables",
                    "AttributeEffects", "LinkedVariables"
                ), "          ")

                effects = as_list(get(entry, "AttributeEffects"))
                for j, effect in enumerate(effects[:MAX_ITEMS]):
                    print(f"          AttributeEffect [{j}]: {path(effect)}")
                    show_fields(effect, (
                        "AttributeToModify", "ModifierType",
                        "BaseModifierValue", "ModifierValue", "BaseValue"
                    ), "            ")

print("\n=== End diagnostic; no game state was changed ===")
