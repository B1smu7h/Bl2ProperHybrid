# Runtime Diagnostic Plan (Proton GE)

This is the first local investigation step for BL2 Proper Hybrid. It is intentionally non-mutating: it should inspect/log the runtime environment before we experiment with weapon generation.

## Current user-provided setup

- Borderlands 2, vanilla stock installation.
- Linux via Proton GE.
- Standby level 80 Salvador save.
- Exact storefront/build and DLC coverage: not yet confirmed.

## SDK approach

The current pyunrealsdk project documents:
- An embedded Python interpreter.
- The `py` console command for one-line or heredoc-like snippets.
- The `pyexec` command for executing a script file relative to the game working directory.
- An initialization script (default `__main__.py` next to `pyunrealsdk.dll`).
- Runtime object lookup through `unrealsdk.find_object` and `find_all`.
- Function hooks through `unrealsdk.hooks.add_hook`.

Reference: https://github.com/bl-sdk/pyunrealsdk (Readme.md, accessed 2026-10-25).

## First test objective

Before attempting to modify parts or drops, verify the SDK is installed and initialized, then run a read-only query from its embedded interpreter. For example, after the SDK loader is successfully installed, use the in-game console with the documented `py` command:

```python
py print("BL2 Proper Hybrid diagnostic: Python SDK command reached")
```

This is only a smoke test for the console command; it does not prove object inspection works. The next query should be adapted to the installed SDK version and executed only after confirming the first test works:

```python
py << EOF
import unrealsdk
print("SDK module:", unrealsdk)
print("Engine:", unrealsdk.find_object("WillowGameEngine", "Transient.WillowGameEngine_0"))
EOF
```

If the in-game console cannot accept multi-line input, run the same logic in a script file through the documented `pyexec` command, or put it in the configured initialization script. Do not assume a particular console key binding; use the key configured in your game/mod-loader setup.

## What to report back

Please send:
1. Whether BL2 is Steam or Epic.
2. Proton GE version.
3. Whether the SDK / mod loader is already installed. If yes, which one and the installation path.
4. Exact output from the smoke test, or the relevant log/error text if it fails.
5. Confirm that the Salvador save has been copied/backed up before later mutation tests.

## Safety

Do not change part lists or spawn/edit items in this first step. Keep the game vanilla except for the loader required to run the diagnostic. Save all mutation tests for a separate copy of the character.
