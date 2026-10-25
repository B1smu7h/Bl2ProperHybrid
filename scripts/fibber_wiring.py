"""Read-only BL2 SDK diagnostic for Fibber and Evil Smasher behavior wiring.

Run from the SDK Python console:
    pyexec fibber_wiring.py

This script does not intentionally modify game state.
SDK wrappers expose different property names across versions, so unavailable
fields are skipped rather than treated as errors.
"""

import unrealsdk

TOKENS = ("fibber", "evilsmash")
MAX_ITEMS = 24


def safe_get(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default


def obj_path(obj):
    if obj is None:
        return "<none>"

    for name in ("PathName", "FullName", "Name"):
        value = safe_get(obj, name)
        if value is not None:
            try:
                value = value() if callable(value) else value
                return str(value)
            except Exception:
                pass

    return str(obj)


def short(value, limit=180):
    text = (
        obj_path(value)
        if not isinstance(value, (str, int, float, bool))
        else repr(value)
    )
    return text if len(text) <= limit else text[:limit] + "..."


def items(value):
    if value is None:
        return []
    try:
        return list(value)
    except Exception:
        return []


def print_fields(obj, names, indent="    "):
    for name in names:
        value = safe_get(obj, name)
        if value is not None:
            print(f"{indent}{name}: {short(value)}")


print("=== BL2 behavior wiring diagnostic (READ ONLY) ===")

try:
    providers = list(unrealsdk.find_all("BehaviorProviderDefinition"))
except Exception as exc:
    print("Could not enumerate BehaviorProviderDefinition objects:", repr(exc))
    raise

matches = []
for provider in providers:
    path = obj_path(provider)
    if any(token in path.lower() for token in TOKENS):
        matches.append(provider)

print(f"Matching providers: {len(matches)}")

for provider in matches:
    print("\n" + "=" * 72)
    print("PROVIDER:", obj_path(provider))

    sequences = safe_get(provider, "BehaviorSequences")
    if sequences is None:
        sequences = safe_get(provider, "Sequences")

    seqs = items(sequences)
    print(
        "Sequence collection:",
        "found" if sequences is not None else "not exposed",
        f"({len(seqs)} entries)",
    )

    for si, seq in enumerate(seqs[:MAX_ITEMS]):
        print(f"\n  SEQUENCE [{si}]: {obj_path(seq)}")
        print_fields(
            seq,
            (
                "SequenceName",
                "Name",
                "bEnabledOnSpawn",
                "EnabledOnSpawn",
                "EventData2",
                "BehaviorData2",
                "OutputLinks",
                "OutputVariables",
            ),
            "    ",
        )

        for field in (
            "EventData2",
            "BehaviorData2",
            "OutputLinks",
            "OutputVariables",
        ):
            collection = safe_get(seq, field)
            entries = items(collection)
            if not entries:
                continue

            print(f"    {field}: {len(entries)} entries")
            for i, entry in enumerate(entries[:MAX_ITEMS]):
                print(f"      [{i}] {obj_path(entry)}")
                print_fields(
                    entry,
                    (
                        "Event",
                        "EventName",
                        "Name",
                        "bEnabled",
                        "Enabled",
                        "OutputLinks",
                        "OutputVariables",
                        "Behavior",
                        "BehaviorSequence",
                        "SkillToActivate",
                        "SkillToDeactivate",
                        "AttributeEffects",
                        "LinkedVariables",
                    ),
                    "        ",
                )

                effects = safe_get(entry, "AttributeEffects")
                for j, effect in enumerate(items(effects)[:MAX_ITEMS]):
                    print(f"        AttributeEffect [{j}]: {obj_path(effect)}")
                    print_fields(
                        effect,
                        (
                            "AttributeToModify",
                            "ModifierType",
                            "BaseModifierValue",
                            "ModifierValue",
                            "BaseValue",
                        ),
                        "          ",
                    )

print("\n=== End diagnostic; no game state was changed ===")
