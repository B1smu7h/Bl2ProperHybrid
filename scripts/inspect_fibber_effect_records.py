"""Inspect nested attribute-effect records on Fibber barrel objects.

Run in the SDK console with:
    pyexec scripts/inspect_fibber_effect_records.py

Read-only diagnostic: no hooks, object mutation, or save access.
"""
import unrealsdk

PARTS = (
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3"),
)

PROVIDER_PATHS = (
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1:BehaviorProviderDefinition_3"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2:BehaviorProviderDefinition_3"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3:BehaviorProviderDefinition_3"),
)

def brief(value, limit=850):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

def safe_attr(obj, name):
    try:
        return getattr(obj, name)
    except Exception:
        return None

def relevant_names(obj):
    try:
        names = [name for name in dir(obj) if not name.startswith("__")]
        keys = ("attribute", "modifier", "value", "effect", "weapon", "class", "name", "outer")
        return [name for name in names if any(key in name.lower() for key in keys)]
    except Exception:
        return []

def inspect_records(label, source_name, records, limit=12):
    print(f"  {source_name}: {brief(records, 1200)}")
    try:
        count = len(records)
    except Exception:
        print("    Not a sized collection; stopping nested inspection.")
        return
    print("    record count:", count)
    for index, record in enumerate(records):
        if index >= limit:
            print("    ... additional records omitted")
            break
        print(f"    [{index}] {brief(record, 550)}")
        names = relevant_names(record)
        if names:
            print("      relevant fields:", ", ".join(names[:30]))
        for field in (
            "AttributeToModify", "Attribute", "AttributeDefinition", "ModifierType",
            "BaseModifierValue", "BaseValue", "BaseValueConstant", "BaseValueAttribute",
            "InitializationDefinition", "BaseValueScaleConstant", "bIncludeInWeaponStats",
            "Class", "Name",
        ):
            value = safe_attr(record, field)
            if value is not None:
                print(f"      {field} = {brief(value, 300)}")

print("=== BL2 Proper Hybrid: nested Fibber effect records ===")

print("\n## Part WeaponAttributeEffects")
for label, path in PARTS:
    print("\n--", label, "--")
    try:
        part = unrealsdk.find_object("WeaponPartDefinition", path)
        print("Part:", repr(part))
        records = part.WeaponAttributeEffects
        inspect_records(label, "WeaponAttributeEffects", records)
    except Exception as exc:
        print("Part/effect lookup failed:", type(exc).__name__, str(exc))

print("\n## Behavior_AttributeEffect AttributeEffects")
for label, path in PROVIDER_PATHS:
    print("\n--", label, "--")
    try:
        provider = unrealsdk.find_object("BehaviorProviderDefinition", path)
        sequence = provider.BehaviorSequences[0]
    except Exception as exc:
        print("Provider lookup failed:", type(exc).__name__, str(exc))
        continue

    seen = 0
    for field in ("BehaviorData", "BehaviorData2"):
        entries = safe_attr(sequence, field) or []
        for entry in entries:
            behavior = safe_attr(entry, "Behavior")
            if behavior is None or "Behavior_AttributeEffect" not in str(safe_attr(behavior, "Class")):
                continue
            seen += 1
            if seen > 12:
                print("  ... additional behavior effects omitted")
                break
            print("  Behavior:", repr(behavior))
            print("    AttributeEffects exposed names:", ", ".join(relevant_names(behavior)[:35]))
            records = safe_attr(behavior, "AttributeEffects")
            if records is None:
                print("    AttributeEffects property unavailable or None")
            else:
                inspect_records(label, "AttributeEffects", records, limit=8)
        if seen > 12:
            break

print("\n=== Inspection complete; no game state was changed. ===")
