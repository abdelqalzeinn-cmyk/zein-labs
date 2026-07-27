--[[
  EmptyCleaner.lua  -  AgileBot Companion Pack #1
  Deletes Model/Folder instances that have no children.
  Usage:
    local Cleaner = require(script.Parent.EmptyCleaner)
    Cleaner.sweep(game.Workspace)
]]
local module = {}

function module.sweep(parent)
	local removed = 0
	if not parent then return 0 end
	local targets = {}
	for _, inst in ipairs(parent:GetDescendants()) do
		if (inst:IsA("Model") or inst:IsA("Folder")) and #inst:GetChildren() == 0 then
			table.insert(targets, inst)
		end
	end
	for _, inst in ipairs(targets) do
		inst:Destroy()
		removed = removed + 1
	end
	return removed
end

return module
