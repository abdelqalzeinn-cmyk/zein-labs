--[[
  RenameSelected.lua  -  AgileBot Companion Pack #1
  Adds a prefix/suffix to every selected instance's name.
  Usage:
    local Rename = require(script.Parent.RenameSelected)
    Rename.apply(game:GetService("Selection"):Get(), "[old]", nil)
]]
local module = {}

function module.apply(instances, prefix, suffix)
	prefix = prefix or ""
	suffix = suffix or ""
	local n = 0
	for _, inst in ipairs(instances or {}) do
		inst.Name = prefix .. inst.Name .. suffix
		n = n + 1
	end
	return n
end

return module
