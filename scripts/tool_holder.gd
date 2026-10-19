extends Node3D
# Manages which cleaning tool is currently visible and active

var tools: Dictionary = {}
var current_tool_name: String = "mop"
var current_tool: Node3D = null

func _ready() -> void:
	GameManager.tool_changed.connect(_on_tool_changed)
	# Register all child tools by their tool_name property
	for child in get_children():
		if child.has_method("activate"):
			tools[child.tool_name] = child
			child.deactivate()
	# Activate starting tool
	call_deferred("_activate_tool", "mop")

func _on_tool_changed(tool_name: String) -> void:
	_activate_tool(tool_name)

func _activate_tool(tool_name: String) -> void:
	if current_tool:
		current_tool.deactivate()
	if tool_name in tools:
		current_tool = tools[tool_name]
		current_tool.activate()
		current_tool_name = tool_name
		# Tell the player which tool is active
		var player = get_tree().get_first_node_in_group("player")
		if player and player.has_method("equip_tool"):
			player.equip_tool(current_tool)
	else:
		push_warning("Tool not found: " + tool_name)

func switch_to(tool_name: String) -> void:
	_activate_tool(tool_name)
