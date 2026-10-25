"""Read-only runtime diagnostic for BL2 Proper Hybrid.

Run from the BL2 SDK console with:
    pyexec scripts/runtime_diagnostic.py

This script does not install hooks, mutate game objects, or touch save data.
"""
import sys

print("=== BL2 Proper Hybrid: runtime diagnostic ===")
print("Python:", sys.version)

try:
    import unrealsdk
    print("unrealsdk import: OK")
    print("unrealsdk module:", unrealsdk)
except Exception as exc:
    print("unrealsdk import: FAILED:", type(exc).__name__, str(exc))
    raise

try:
    engine = unrealsdk.find_object(
        "WillowGameEngine",
        "Transient.WillowGameEngine_0",
    )
    print("WillowGameEngine lookup:", repr(engine))
except Exception as exc:
    print("WillowGameEngine lookup failed:", type(exc).__name__, str(exc))

print("=== Diagnostic complete; no game state was changed. ===")
