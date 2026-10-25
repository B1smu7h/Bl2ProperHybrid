"""Inspect selected unique weapon parts and their property surfaces.

Run in the SDK console with:
    pyexec scripts/inspect_unique_parts.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

PARTS = (
    ("Evil Smasher barrel", "GD_Weap_AssaultRifle.Barrel.AR_Barrel_Vladof_EvilSmasher"),
    ("Evil Smasher material", "GD_Weap_AssaultRifle.ManufacturerMaterials.Mat_Torgue_3_EvilSmasher"),
    ("Fibber barrel 1", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_1"),
    ("Fibber barrel 2", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_2"),
    ("Fibber barrel 3", "GD_Weap_Pistol.Barrel.Fibber.Pistol_Barrel_Bandit_Fibber_3"),
    ("Conference Call barrel", "GD_Weap_Shotgun.Barrel.SG_Barrel_Hyperion_ConferenceCall"),
)

CANDIDATE_FIELDS = (
    "WeaponAttributeEffects",
    "AttributeSlotEffects",
    "BehaviorProviderDefinition",
    "BehaviorProviderDefinitions",
    "WeaponTypeDefinition",
    "PartType",
    "Manufacturer",
    "BaseDefinition",
    "Class",
    "Outer",
    "Name",
)

def brief(value, limit=900):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: unique part inspection ===")
for label, path in PARTS:
    print("\n##", label)
    obj = None
    try:
        obj = unrealsdk.find_object("WeaponPartDefinition", path)
        print("Object:", repr(obj))
    except Exception as exc:
        print("Lookup failed:", type(exc).__name__, str(exc))
        continue

    try:
        names = [n for n in dir(obj) if not n.startswith("__")]
        relevant = [n for n in names if any(key in n.lower() for key in (
            "effect", "behavior", "attribute", "part", "weapon", "manufacturer",
            "damage", "projectile", "fire", "class", "outer", "name"
        ))]
        print("Relevant exposed names:", ", ".join(relevant)[:1600])
    except Exception as exc:
        print("Name inspection failed:", type(exc).__name__, str(exc))

    for field in CANDIDATE_FIELDS:
        try:
            print(f"  {field} = {brief(getattr(obj, field))}")
        except Exception as exc:
            print(f"  {field}: unavailable ({type(exc).__name__}: {exc})")

print("\n=== Inspection complete; no game state was changed. ===")
