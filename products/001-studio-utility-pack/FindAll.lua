--[[
  FindAll.lua  -  AgileBot Companion Pack #1
  Returns a table of every instance of `className` under `parent`.
  Usage (in Studio command bar or a Script):
    local FindAll = require(script.Parent.FindAll)
    local parts = FindAll(game.Workspace, "BasePart")
]]
local module = {}

function module.find(parent, className)
	local results = {}
	if not parent then return results end
	for _, child in ipairs(parent:GetDescendants()) do
		if child:IsA(className) then
			table.insert(results, child)
		end
	end
	return results
end

return module
