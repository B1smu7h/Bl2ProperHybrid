"""Inspect attribute effects referenced by Fibber barrel behavior providers.

Run in the SDK console with:
    pyexec scripts/inspect_attribute_effects.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

PROVIDERS = (
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1:BehaviorProviderDefinition_3"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2:BehaviorProviderDefinition_3"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3:BehaviorProviderDefinition_3"),
)

def brief(value, limit=420):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

def obj_name(obj):
    if obj is None:
        return "None"
    try:
        return str(obj.PathName(obj))
    except Exception:
        return repr(obj)

print("=== BL2 Proper Hybrid: attribute effect inspection ===")
for label, path in PROVIDERS:
    print("\n##", label)
    try:
        provider = unrealsdk.find_object("BehaviorProviderDefinition", path)
        sequences = provider.BehaviorSequences
    except Exception as exc:
        print("Provider lookup failed:", type(exc).__name__, str(exc))
        continue

    for seq_index, sequence in enumerate(sequences):
        for data_field in ("BehaviorData", "BehaviorData2"):
            entries = getattr(sequence, data_field, [])
            for entry in entries:
                behavior = getattr(entry, "Behavior", None)
                if behavior is None:
                    continue
                if "Behavior_AttributeEffect" not in str(getattr(behavior, "Class", "")):
                    continue
                print(f"  {data_field}: {obj_name(behavior)}")
                try:
                    names = [n for n in dir(behavior) if not n.startswith("__")]
                    relevant = [n for n in names if any(key in n.lower() for key in (
                        "attribute", "modifier", "value", "effect", "duration", "stack", "class", "name"
                    ))]
                    print("    exposed:", ", ".join(relevant)[:900])
                except Exception:
                    pass
                for field in (
                    "AttributeToModify", "ModifierType", "BaseModifierValue",
                    "BaseValue", "InitializationDefinition", "Duration",
                    "bUseWeaponMelee", "Class", "Outer", "Name",
                ):
                    try:
                        print(f"    {field} = {brief(getattr(behavior, field))}")
                    except Exception as exc:
                        print(f"    {field}: unavailable ({type(exc).__name__})")

print("\n=== Inspection complete; no game state was changed. ===")
