# Runtime Diagnostic Plan (Proton GE)

This is the first local investigation step for BL2 Proper Hybrid. It is intentionally non-mutating: inspect the runtime and log useful objects before experimenting with weapon generation.

## Current setup (reported)

- Borderlands 2, vanilla stock installation.
- Linux through Proton GE.
- A standby level 80 Salvador save is available.
- Exact storefront/build and DLC coverage: not yet confirmed.

## Important loader note

The current UnrealSDK README says it does not load itself: BL2 needs a game-specific plugin loader. It explicitly warns that simply renaming `unrealsdk.dll` to `d3d9.dll` is not a valid installation procedure. Do not manually copy/rename the SDK DLL based on old tutorials.

References:
- UnrealSDK: https://github.com/bl-sdk/unrealsdk
- pyunrealsdk: https://github.com/bl-sdk/pyunrealsdk

The pyunrealsdk documentation describes:
- An embedded Python interpreter.
- `py` for short Python snippets (including heredoc-like multi-line code).
- `pyexec` for executing a script file relative to the game working directory.
- An initialization script (default `__main__.py` next to `pyunrealsdk.dll`).
- Object lookup through `unrealsdk.find_object` and `find_all`.
- Runtime function hooks through `unrealsdk.hooks.add_hook`.

## Before installing anything

Please first confirm:
1. Is this the Steam or Epic version of BL2?
2. What Proton GE version are you running?
3. Is any BL2 SDK loader/mod manager already installed? If yes, which one and where?
4. Do you have all official DLC installed, or only some of it?

Keep the game vanilla until we choose a current BL2-compatible loader and follow its official instructions. The presence of a working Proton setup does not by itself prove that the current SDK loader is installed.

## First diagnostic after loader installation is confirmed

Use the in-game console's documented Python command to run this non-mutating smoke test:

```python
py print("BL2 Proper Hybrid diagnostic: Python SDK command reached")
```

If the command succeeds, check the SDK module and a known engine object:

```python
py << EOF
import unrealsdk
print("SDK module:", unrealsdk)
print("Engine:", unrealsdk.find_object("WillowGameEngine", "Transient.WillowGameEngine_0"))
EOF
```

If the in-game console cannot accept the multi-line block, run a script file using the documented `pyexec` command or use the configured initialization script. Do not assume a particular console key binding; follow the key set by the chosen loader/game config.

## What to send back

- Storefront and Proton GE version.
- Whether a loader is already installed.
- Exact output from the smoke test, or relevant log/error text if it fails.
- Confirmation that the Salvador save has been copied before later mutation tests.

## Safety

Do not edit part lists, mutate weapon objects, or spawn/edit items during the first test. Use a separate save copy for all later item-validation and persistence experiments.
