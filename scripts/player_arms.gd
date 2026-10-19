# scripts/player_arms.gd
extends Node3D
class_name PlayerArms

enum ToolType { MOP, SPONGE, BROOM, SPRAY }

const TOOL_NAME_MAP = {
	ToolType.MOP: "mop",
	ToolType.SPONGE: "sponge",
	ToolType.BROOM: "broom",
	ToolType.SPRAY: "spray",
}

@export var current_tool: ToolType = ToolType.MOP:
	set(value):
		current_tool = value
		_update_equipped_tool()
		_sync_tool_to_game_manager()

@export_group("Sway & Bob Settings")
@export var mouse_sway_amount: float = 0.0025
@export var max_sway_offset: float = 0.08
@export var sway_smooth_speed: float = 10.0
@export var bob_frequency: float = 9.5
@export var bob_amplitude: float = 0.035

@onready var right_arm_pivot: Node3D = $RightArmPivot
@onready var left_arm_pivot: Node3D = $LeftArmPivot
@onready var tool_socket: Node3D = $RightArmPivot/RightGloveMesh/ToolSocket

@onready var tool_nodes: Dictionary = {
	ToolType.MOP: $RightArmPivot/RightGloveMesh/ToolSocket/MopMesh,
	ToolType.SPONGE: $RightArmPivot/RightGloveMesh/ToolSocket/SpongeMesh,
	ToolType.BROOM: $RightArmPivot/RightGloveMesh/ToolSocket/BroomMesh,
	ToolType.SPRAY: $RightArmPivot/RightGloveMesh/ToolSocket/SprayMesh,
}

var _base_pos_r: Vector3
var _base_pos_l: Vector3
var _base_rot_r: Vector3
var _mouse_input: Vector2 = Vector2.ZERO
var _bob_time: float = 0.0
var _swing_time: float = 0.0
var _is_swinging: bool = false

func _ready() -> void:
	_base_pos_r = right_arm_pivot.position
	_base_pos_l = left_arm_pivot.position
	_base_rot_r = right_arm_pivot.rotation
	_update_equipped_tool()
	
	if Engine.has_singleton("GameManager") or get_node_or_null("/root/GameManager"):
		GameManager.tool_changed.connect(_on_game_manager_tool_changed)
		_on_game_manager_tool_changed(GameManager.current_tool)

func _on_game_manager_tool_changed(tname: String) -> void:
	match tname.to_lower():
		"mop":
			if current_tool != ToolType.MOP:
				current_tool = ToolType.MOP
		"sponge":
			if current_tool != ToolType.SPONGE:
				current_tool = ToolType.SPONGE
		"broom":
			if current_tool != ToolType.BROOM:
				current_tool = ToolType.BROOM
		"spray":
			if current_tool != ToolType.SPRAY:
				current_tool = ToolType.SPRAY

func _sync_tool_to_game_manager() -> void:
	if not is_inside_tree():
		return
	if Engine.has_singleton("GameManager") or get_node_or_null("/root/GameManager"):
		var t_name: String = TOOL_NAME_MAP.get(current_tool, "mop")
		if GameManager.current_tool != t_name:
			GameManager.set_tool(t_name)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		_mouse_input = event.relative
	elif event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_1: current_tool = ToolType.MOP
			KEY_2: current_tool = ToolType.SPONGE
			KEY_3: current_tool = ToolType.BROOM
			KEY_4: current_tool = ToolType.SPRAY
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		trigger_tool_action()

func _process(delta: float) -> void:
	# Fetch horizontal speed from parent CharacterBody3D if attached to Player
	var move_speed: float = 0.0
	var player: CharacterBody3D = null
	var n: Node = get_parent()
	while n:
		if n is CharacterBody3D:
			player = n
			break
		n = n.get_parent()

	if player:
		var h_vel := Vector2(player.velocity.x, player.velocity.z)
		move_speed = h_vel.length()

	# 1. Walk Cycle Bobbing
	if move_speed > 0.2:
		_bob_time += delta * bob_frequency * clampf(move_speed / 5.0, 0.5, 1.8)
	else:
		_bob_time = lerpf(_bob_time, 0.0, delta * 5.0)

	var bob_x := cos(_bob_time * 0.5) * bob_amplitude
	var bob_y := absf(sin(_bob_time)) * bob_amplitude

	# 2. Mouse Rotational Inertia Sway
	var sway_x := clampf(-_mouse_input.x * mouse_sway_amount, -max_sway_offset, max_sway_offset)
	var sway_y := clampf(_mouse_input.y * mouse_sway_amount, -max_sway_offset, max_sway_offset)
	_mouse_input = _mouse_input.lerp(Vector2.ZERO, delta * 12.0)

	var target_r := _base_pos_r + Vector3(bob_x + sway_x, bob_y + sway_y, 0.0)
	var target_l := _base_pos_l + Vector3(-bob_x + sway_x * 0.8, bob_y * 0.8 + sway_y, 0.0)

	right_arm_pivot.position = right_arm_pivot.position.lerp(target_r, delta * sway_smooth_speed)
	left_arm_pivot.position = left_arm_pivot.position.lerp(target_l, delta * sway_smooth_speed)

	# 3. Slapstick Tool Sweeping / Scrubbing Animation
	if _is_swinging:
		_swing_time += delta * 12.0
		var sweep_cycle := sin(_swing_time)
		var sweep_cos := cos(_swing_time)

		match current_tool:
			ToolType.MOP:
				# Fluid figure-8 sweeping & push-pull across the floor (no pickaxe wacking!)
				var mop_sway_x = sweep_cycle * 0.16
				var mop_push_z = sweep_cos * 0.09
				right_arm_pivot.position = target_r + Vector3(mop_sway_x, -0.04 + absf(sweep_cycle) * 0.02, mop_push_z)
				right_arm_pivot.rotation = _base_rot_r + Vector3(-0.06, sweep_cycle * 0.28, sweep_cycle * 0.18)
				# Left assist arm coordinates with sweeping handle motion
				left_arm_pivot.position = target_l + Vector3(mop_sway_x * 0.8, -0.03, mop_push_z * 0.8)
				left_arm_pivot.rotation.y = sweep_cycle * 0.22

			ToolType.BROOM:
				# Brisk, rhythmic side-to-side sweeping flick across the floor
				var broom_stroke := sin(_swing_time * 1.4)
				var broom_flick := cos(_swing_time * 1.4)
				right_arm_pivot.position = target_r + Vector3(broom_stroke * 0.15, -0.03, broom_flick * 0.06)
				right_arm_pivot.rotation = _base_rot_r + Vector3(-0.04, broom_stroke * 0.40, broom_stroke * 0.22)
				left_arm_pivot.position = target_l + Vector3(broom_stroke * 0.6, -0.02, 0.0)

			ToolType.SPONGE:
				# Circular surface scrubbing & gentle forward thrust (kept intact as requested)
				var scrub_x := cos(_swing_time * 2.0) * 0.06
				var scrub_y := sin(_swing_time * 2.0) * 0.04
				right_arm_pivot.position = target_r + Vector3(scrub_x, scrub_y, -0.12 - absf(sin(_swing_time)) * 0.06)
				right_arm_pivot.rotation = _base_rot_r + Vector3(0.12, 0.0, scrub_x * 0.4)

			ToolType.SPRAY:
				# Trigger pump recoil with mist tilt
				var spray_pulse := sin(_swing_time)
				right_arm_pivot.position = target_r + Vector3(0.0, spray_pulse * 0.02, spray_pulse * 0.05)
				right_arm_pivot.rotation.x = _base_rot_r.x + spray_pulse * 0.15

		if _swing_time >= TAU:
			if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
				_swing_time = 0.0
			else:
				_is_swinging = false
				_swing_time = 0.0
	else:
		right_arm_pivot.rotation = right_arm_pivot.rotation.lerp(_base_rot_r, delta * sway_smooth_speed)
		left_arm_pivot.rotation = left_arm_pivot.rotation.lerp(Vector3.ZERO, delta * sway_smooth_speed)

func trigger_tool_action() -> void:
	if not _is_swinging:
		_is_swinging = true
		_swing_time = 0.0

func _update_equipped_tool() -> void:
	if not is_node_ready():
		return
	for t_key in tool_nodes:
		if is_instance_valid(tool_nodes[t_key]):
			tool_nodes[t_key].visible = (t_key == current_tool)
	# Adjust left assist hand for two-handed pole tools vs one-handed tools
	if is_instance_valid(left_arm_pivot):
		var is_pole := (current_tool == ToolType.MOP or current_tool == ToolType.BROOM)
		_base_pos_l = Vector3(-0.14, -0.22, -0.42) if is_pole else Vector3(-0.28, -0.30, -0.35)