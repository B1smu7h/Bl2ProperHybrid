"""Inspect behavior-provider references used by selected weapon parts.

Run in the SDK console with:
    pyexec scripts/inspect_behavior_providers.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

PROVIDERS = (
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1:BehaviorProviderDefinition_3"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2:BehaviorProviderDefinition_3"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3:BehaviorProviderDefinition_3"),
    ("Evil Smasher barrel", "GD_Weap_AssaultRifle.Barrel.AR_Barrel_Vladof_EvilSmasher:BehaviorProviderDefinition_16"),
)

FIELDS = (
    "BehaviorSequences",
    "BehaviorData",
    "BehaviorEvents",
    "DefaultBehavior",
    "Class",
    "Outer",
    "Name",
)

def brief(value, limit=1400):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: behavior provider inspection ===")
for label, path in PROVIDERS:
    print("\n##", label)
    try:
        obj = unrealsdk.find_object("BehaviorProviderDefinition", path)
        print("Object:", repr(obj))
    except Exception as exc:
        print("Lookup failed:", type(exc).__name__, str(exc))
        continue

    try:
        names = [n for n in dir(obj) if not n.startswith("__")]
        relevant = [n for n in names if any(key in n.lower() for key in (
            "behavior", "sequence", "event", "provider", "definition", "class", "outer", "name"
        ))]
        print("Relevant exposed names:", ", ".join(relevant)[:1500])
    except Exception as exc:
        print("Name inspection failed:", type(exc).__name__, str(exc))

    for field in FIELDS:
        try:
            print(f"  {field} = {brief(getattr(obj, field))}")
        except Exception as exc:
            print(f"  {field}: unavailable ({type(exc).__name__}: {exc})")

print("\n=== Inspection complete; no game state was changed. ===")
