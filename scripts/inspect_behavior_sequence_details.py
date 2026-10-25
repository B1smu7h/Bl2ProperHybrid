"""Summarize behavior sequences and referenced behavior objects.

Run in the SDK console with:
    pyexec scripts/inspect_behavior_sequence_details.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

PROVIDERS = (
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1:BehaviorProviderDefinition_3"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2:BehaviorProviderDefinition_3"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3:BehaviorProviderDefinition_3"),
    ("Evil Smasher barrel", "GD_Weap_AssaultRifle.Barrel.AR_Barrel_Vladof_EvilSmasher:BehaviorProviderDefinition_16"),
)

def safe_attr(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default

def obj_name(obj):
    if obj is None:
        return "None"
    try:
        return str(obj.PathName(obj))
    except Exception:
        return repr(obj)

def brief(value, limit=260):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: behavior sequence details ===")
for label, path in PROVIDERS:
    print("\n##", label)
    try:
        provider = unrealsdk.find_object("BehaviorProviderDefinition", path)
        sequences = provider.BehaviorSequences
        print("Provider:", obj_name(provider), "| sequences:", len(sequences))
    except Exception as exc:
        print("Provider lookup failed:", type(exc).__name__, str(exc))
        continue

    for seq_index, sequence in enumerate(sequences):
        print(f"  Sequence {seq_index}: name={safe_attr(sequence, 'BehaviorSequenceName')!r}, enabled_on_spawn={safe_attr(sequence, 'bEnabledOnSpawn')!r}")
        for event_field in ("EventData", "EventData2"):
            events = safe_attr(sequence, event_field, [])
            if events:
                print(f"    {event_field}:")
                for event in list(events)[:8]:
                    print("      ", brief(event, 350))

        for data_field in ("BehaviorData", "BehaviorData2"):
            entries = safe_attr(sequence, data_field, [])
            if entries:
                print(f"    {data_field}: {len(entries)} entries")
                for entry_index, entry in enumerate(list(entries)[:18]):
                    behavior = safe_attr(entry, "Behavior")
                    print(f"      [{entry_index}] {obj_name(behavior)}")
                    if behavior is not None:
                        for field in ("Class", "Outer", "Name", "AttributeToModify", "ModifierType", "BaseModifierValue", "SkillToActivate", "SkillToDeactivate"):
                            value = safe_attr(behavior, field, None)
                            if value is not None:
                                print(f"          {field} = {brief(value, 220)}")
                if len(entries) > 18:
                    print("      ... additional entries omitted")

print("\n=== Inspection complete; no game state was changed. ===")
