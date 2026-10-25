"""Inspect runtime part-list collections referenced by unique weapons.

Run in the SDK console with:
    pyexec scripts/inspect_part_list_collection.py

Read-only exploratory diagnostic. No hooks, mutations, or save access.
"""
import unrealsdk

TARGETS = (
    ("Evil Smasher", "GD_Weap_AssaultRifle.A_Weapons_Unique.AR_Torgue_3_EvilSmasher"),
    ("Fibber", "GD_Weap_Pistol.A_Weapons_Unique.Pistol_Hyperion_3_Fibber"),
    ("Conference Call", "GD_Weap_Shotgun.A_Weapons_Legendary.SG_Hyperion_5_ConferenceCall"),
)

def brief(value, limit=700):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "... [truncated]"

print("=== BL2 Proper Hybrid: part-list collection inspection ===")
for label, path in TARGETS:
    print("\n##", label)
    try:
        balance = unrealsdk.find_object("WeaponBalanceDefinition", path)
        print("Balance:", repr(balance))
        collection = balance.RuntimePartListCollection
        print("RuntimePartListCollection:", repr(collection))
    except Exception as exc:
        print("Balance/collection lookup failed:", type(exc).__name__, str(exc))
        continue

    try:
        names = [n for n in dir(collection) if not n.startswith("__")]
        print("Collection visible names:", ", ".join(names)[:1800])
    except Exception as exc:
        print("Collection name inspection failed:", type(exc).__name__, str(exc))

    for field in (
        "bEnabled",
        "PartLists",
        "WeightedParts",
        "bIsInitialized",
        "Class",
        "Outer",
        "Name",
    ):
        try:
            print(f"  {field} = {brief(getattr(collection, field))}")
        except Exception as exc:
            print(f"  {field}: unavailable ({type(exc).__name__}: {exc})")

print("\n=== Inspection complete; no game state was changed. ===")
