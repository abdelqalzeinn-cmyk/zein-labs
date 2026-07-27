--[[
  BatchAnchor.lua  -  AgileBot Companion Pack #1
  Anchors or un-anchors every BasePart under `parent`.
  Usage:
    local BatchAnchor = require(script.Parent.BatchAnchor)
    BatchAnchor.set(game.Workspace, true)   -- anchor all
]]
local module = {}

function module.set(parent, anchored)
	local count = 0
	if not parent then return 0 end
	for _, part in ipairs(parent:GetDescendants()) do
		if part:IsA("BasePart") then
			part.Anchored = anchored
			count = count + 1
		end
	end
	return count
end

return module
