"""Summarize Fibber barrel modifiers in a compact, readable format.

Run in the SDK console:
    pyexec scripts/summarize_fibber_effects.py

Read-only diagnostic. It prints each part's direct weapon attributes and
Behavior_AttributeEffect records separately so the two layers are not confused.
"""
import unrealsdk

PARTS = (
    ("Fibber 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1",
     "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1:BehaviorProviderDefinition_3"),
    ("Fibber 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2",
     "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2:BehaviorProviderDefinition_3"),
    ("Fibber 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3",
     "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3:BehaviorProviderDefinition_3"),
)

def safe_attr(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default

def short(value, limit=180):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "..."

def object_path(obj):
    if obj is None:
        return "<none>"
    try:
        return obj.GetFullName()
    except Exception:
        return repr(obj)

def modifier_record(record):
    attr = safe_attr(record, "AttributeToModify")
    mod_type = safe_attr(record, "ModifierType")
    base = safe_attr(record, "BaseModifierValue")
    constant = safe_attr(base, "BaseValueConstant")
    attr_path = object_path(attr)
    return attr_path, short(mod_type), short(constant), short(base)

print("=== BL2 Proper Hybrid: concise Fibber effect summary ===")
print("Values are raw exposed fields; interpretation depends on BL2 modifier semantics.")

for label, part_path, provider_path in PARTS:
    print(f"\n## {label}")
    try:
        part = unrealsdk.find_object("WeaponPartDefinition", part_path)
        print("Part:", object_path(part))
        records = safe_attr(part, "WeaponAttributeEffects", []) or []
        print("Direct WeaponAttributeEffects:", len(records))
        for record in records:
            attr, mod_type, constant, base = modifier_record(record)
            print(f"  {attr} | type={mod_type} | constant={constant} | base={base}")
    except Exception as exc:
        print("Part inspection failed:", type(exc).__name__, str(exc))

    try:
        provider = unrealsdk.find_object("BehaviorProviderDefinition", provider_path)
        sequences = safe_attr(provider, "BehaviorSequences", []) or []
        print("Behavior provider:", object_path(provider), "| sequences:", len(sequences))
    except Exception as exc:
        print("Provider inspection failed:", type(exc).__name__, str(exc))
        continue

    seen = set()
    for sequence_index, sequence in enumerate(sequences):
        for collection_name in ("BehaviorData", "BehaviorData2"):
            entries = safe_attr(sequence, collection_name, []) or []
            for entry in entries:
                behavior = safe_attr(entry, "Behavior")
                if behavior is None or "Behavior_AttributeEffect" not in str(safe_attr(behavior, "Class", "")):
                    continue
                effect_path = object_path(behavior)
                if effect_path in seen:
                    continue
                seen.add(effect_path)
                records = safe_attr(behavior, "AttributeEffects", []) or []
                print(f"  Behavior effect: {effect_path} | records={len(records)}")
                for record in records:
                    attr, mod_type, constant, base = modifier_record(record)
                    print(f"    {attr} | type={mod_type} | constant={constant} | base={base}")

print("\n=== Summary complete; no game state was changed. ===")
