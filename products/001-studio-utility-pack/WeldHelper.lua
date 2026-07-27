--[[
  WeldHelper.lua  -  AgileBot Companion Pack #1
  Creates a WeldConstraint between `partA` and `partB`.
  Usage:
    local Weld = require(script.Parent.WeldHelper)
    Weld.link(workspace.PartA, workspace.PartB)
]]
local module = {}

function module.link(partA, partB)
	if not (partA and partB) then return nil end
	local weld = Instance.new("WeldConstraint")
	weld.Part0 = partA
	weld.Part1 = partB
	weld.Parent = partA
	return weld
end

return module
