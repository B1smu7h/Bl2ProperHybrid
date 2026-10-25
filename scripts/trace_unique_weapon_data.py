"""Trace candidate data objects for selected BL2 unique weapons.

Run in the SDK console with:
    pyexec scripts/trace_unique_weapon_data.py

This is exploratory and read-only. It does not mutate objects, install hooks,
or touch save data.
"""
import unrealsdk

TARGETS = (
    "EvilSmasher",
    "Fibber",
    "ConferenceCall",
    "Lyuda",
    "Butcher",
    "Gunerang",
)

SEARCH_CLASSES = (
    "WeaponPartDefinition",
    "WeaponNamePartDefinition",
    "InventoryBalanceDefinition",
    "WeaponBalanceDefinition",
)

print("=== BL2 Proper Hybrid: unique weapon data trace ===")
for class_name in SEARCH_CLASSES:
    print("\n-- Searching", class_name, "--")
    try:
        objects = unrealsdk.find_all(class_name, exact=False)
        matches = []
        for obj in objects:
            text = repr(obj)
            if any(target.lower() in text.lower() for target in TARGETS):
                matches.append(text)
        print("Matches:", len(matches))
        for item in matches[:30]:
            print(" ", item)
        if len(matches) > 30:
            print(" ...", len(matches) - 30, "additional matches omitted")
    except Exception as exc:
        print("Query failed:", type(exc).__name__, str(exc))

print("\n=== Trace complete; no game state was changed. ===")
