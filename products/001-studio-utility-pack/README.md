# AgileBot Companion Pack #1 — Studio Utility Scripts

Five drop-in Roblox Studio Lua utilities. Each file is a `ModuleScript`;
require it from your own Script or Plugin and call the returned function.

| File | What it does |
|------|--------------|
| `FindAll.lua` | Collect every instance of a class under a parent. |
| `BatchAnchor.lua` | Anchor / un-anchor all BaseParts under a parent. |
| `RenameSelected.lua` | Add a prefix/suffix to selected instances. |
| `EmptyCleaner.lua` | Delete empty Models/Folders in a tree. |
| `WeldHelper.lua` | Weld two parts with a WeldConstraint. |

## Install
1. In Studio, right-click a folder in Explorer → `Insert Object` → `ModuleScript`.
2. Paste a file's contents in.
3. Require it from your code: `local X = require(path.to.X)`.

All scripts are plain Lua 5.1 / Luau compatible — no plugins or paid tools required.
