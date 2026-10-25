"""Inspect known weapon part-category fields on BL2 part-list collections.

Run in the SDK console with:
    pyexec scripts/inspect_part_category_data.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

TARGETS = (
    ("Evil Smasher", "GD_Weap_AssaultRifle.A_Weapons_Unique.AR_Torgue_3_EvilSmasher"),
    ("Fibber", "GD_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_Fibber"),
    ("Conference Call", "GD_Weap_Shotgun.A_Weapons_Legendary.SG_Hyperion_5_ConferenceCall"),
)

FIELDS = (
    "AssociatedWeaponType",
    "BarrelPartData",
    "BodyPartData",
    "Accessory1PartData",
    "Accessory2PartData",
    "GripPartData",
    "StockPartData",
    "SightPartData",
    "ElementalPartData",
    "ManufacturerPartData",
    "MaterialPartData",
    "PrefixPartData",
    "TitlePartData",
)

def brief(value, limit=1200):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: part-category data inspection ===")
for label, path in TARGETS:
    print("\n##", label)
    try:
        balance = unrealsdk.find_object("WeaponBalanceDefinition", path)
        collection = balance.RuntimePartListCollection
        print("Collection:", repr(collection))
    except Exception as exc:
        print("Lookup failed:", type(exc).__name__, str(exc))
        continue

    for field in FIELDS:
        try:
            value = getattr(collection, field)
            print(f"\n  {field} = {brief(value)}")
            if value is not None and not isinstance(value, (str, int, float, bool)):
                try:
                    names = [n for n in dir(value) if not n.startswith("__")]
                    print("    nested names:", ", ".join(names)[:700])
                except Exception:
                    pass
        except Exception as exc:
            print(f"\n  {field}: unavailable ({type(exc).__name__}: {exc})")

print("\n=== Inspection complete; no game state was changed. ===")
