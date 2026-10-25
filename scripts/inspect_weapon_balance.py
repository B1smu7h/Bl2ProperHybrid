"""Inspect selected fields on a weapon balance definition.

Run in the SDK console with:
    pyexec scripts/inspect_weapon_balance.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

TARGETS = (
    ("Evil Smasher", "GD_Weap_AssaultRifle.A_Weapons_Unique.AR_Torgue_3_EvilSmasher"),
    ("Fibber", "GD_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_Fibber"),
    ("Conference Call", "GD_Weap_Shotgun.A_Weapons_Legendary.SG_Hyperion_5_ConferenceCall"),
)

CANDIDATE_FIELDS = (
    "WeaponTypeDefinition",
    "Manufacturers",
    "Manufacturer",
    "PartListCollection",
    "RuntimePartListCollection",
    "InventoryDefinition",
    "BalanceDefinitionState",
    "bIsUniqueWeapon",
    "InventoryClass",
    "Class",
)

def short_repr(value, limit=500):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: balance property inspection ===")
for label, path in TARGETS:
    print("\n##", label)
    obj = None
    try:
        obj = unrealsdk.find_object("WeaponBalanceDefinition", path)
        print("Object:", repr(obj))
    except Exception as exc:
        print("Lookup failed:", type(exc).__name__, str(exc))
        continue

    try:
        print("Class metadata:", short_repr(obj.Class))
        print("Python-visible names:", ", ".join(name for name in dir(obj) if not name.startswith("__"))[:1200])
    except Exception as exc:
        print("Metadata inspection failed:", type(exc).__name__, str(exc))

    for field in CANDIDATE_FIELDS:
        try:
            value = getattr(obj, field)
            print(f"  {field} = {short_repr(value)}")
        except Exception as exc:
            print(f"  {field}: unavailable ({type(exc).__name__}: {exc})")

print("\n=== Inspection complete; no game state was changed. ===")
