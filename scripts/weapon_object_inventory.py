"""Read-only inventory of selected BL2 weapon-related Unreal objects.

Run in the SDK console with:
    pyexec scripts/weapon_object_inventory.py

This script does not add hooks, mutate game objects, or touch save data.
"""
import unrealsdk

CANDIDATE_CLASSES = (
    "WillowWeapon",
    "WillowWeaponDefinition",
    "WeaponTypeDefinition",
    "WeaponPartDefinition",
    "InventoryBalanceDefinition",
    "InventoryCardItemDefinition",
)

print("=== BL2 Proper Hybrid: weapon object inventory ===")

for class_name in CANDIDATE_CLASSES:
    print("\n-- Class query:", class_name, "--")
    try:
        objects = list(unrealsdk.find_all(class_name, exact=False))
        print("Count:", len(objects))
        for obj in objects[:8]:
            print(" ", repr(obj))
        if len(objects) > 8:
            print(" ...", len(objects) - 8, "more not shown")
    except Exception as exc:
        print("Query failed:", type(exc).__name__, str(exc))

print("\n=== Inventory complete; no game state was changed. ===")
