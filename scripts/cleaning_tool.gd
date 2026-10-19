extends Node3D
# Base cleaning tool - swings when LMB held, cleans nearby dirt spots

@export var tool_name: String = "mop"
@export var reach: float = 2.6
@export var cleaning_rate: float = 1.0
@export var swing_speed: float = 3.5

var is_active: bool = false
var swing_time: float = 0.0
var player: CharacterBody3D = null
var original_rot: Vector3 = Vector3.ZERO
var use_sound_playing: bool = false

func _ready() -> void:
	original_rot = rotation
	await get_tree().process_frame
	player = get_tree().get_first_node_in_group("player")

func use_tool(delta: float) -> void:
	is_active = true
	swing_time += delta * swing_speed
	# Sweeping / scrubbing animation
	var sweep_y = sin(swing_time * 2.5) * 0.35
	var sweep_z = cos(swing_time * 2.5) * 0.15
	rotation.y = lerp(rotation.y, original_rot.y + sweep_y, delta * 12.0)
	rotation.z = lerp(rotation.z, original_rot.z + sweep_z, delta * 12.0)
	# Clean nearby dirt
	_try_clean_nearby(delta)

func _try_clean_nearby(delta: float) -> void:
	if not player:
		player = get_tree().get_first_node_in_group("player")
		if not player:
			return
	var cam = player.get_node_or_null("CameraPivot/Camera3D")
	var origin: Vector3 = cam.global_position if cam else global_position
	var forward: Vector3 = -cam.global_transform.basis.z if cam else -global_transform.basis.z
	var player_pos: Vector3 = player.global_position
	
	# Current active tool name from GameManager
	var active_tool: String = GameManager.current_tool.to_lower() if (Engine.has_singleton("GameManager") or get_node_or_null("/root/GameManager")) else tool_name.to_lower()

	# Generous but bounded reaches (comfortable for high counters, tables, and floor)
	var max_reach: float = 2.4
	if active_tool == "sponge":
		max_reach = 2.3
	elif active_tool == "mop" or active_tool == "broom":
		max_reach = 2.6
	elif active_tool == "spray":
		max_reach = 2.6

	var dirt_spots = get_tree().get_nodes_in_group("dirt_spot")
	var best_spot = null
	var best_score: float = -9999.0

	for spot in dirt_spots:
		if not is_instance_valid(spot) or spot.is_cleaned:
			continue
		# Strictly ignore spots that cannot be cleaned by the currently equipped tool!
		if not spot.can_clean_with(active_tool):
			continue

		var spot_pos: Vector3 = spot.global_position
		var dist_cam: float = origin.distance_to(spot_pos)
		
		# Far-away cutoff
		if dist_cam > max_reach:
			continue
		
		var dir_to_spot: Vector3 = (spot_pos - origin).normalized()
		var aim_dot: float = forward.dot(dir_to_spot)
		
		# Horizontal distance from player feet/center
		var horiz_pos_player = Vector2(player_pos.x, player_pos.z)
		var horiz_pos_spot = Vector2(spot_pos.x, spot_pos.z)
		var horiz_dist: float = horiz_pos_player.distance_to(horiz_pos_spot)
		var height_diff: float = abs(player_pos.y - spot_pos.y)

		var can_clean_this_spot: bool = false
		
		if active_tool == "sponge":
			# Sponge: Must be looking towards it (aim_dot > 0.40)
			# OR standing over/near it (horiz_dist < 1.35 and looking somewhat downwards aim_dot > -0.3)
			var is_looking_at: bool = (aim_dot > 0.40 and dist_cam < max_reach)
			var is_on_top: bool = (horiz_dist < 1.35 and height_diff < 1.8 and aim_dot > -0.3)
			if is_looking_at or is_on_top:
				can_clean_this_spot = true
		elif active_tool == "spray":
			if aim_dot > 0.45 and dist_cam < max_reach:
				can_clean_this_spot = true
		else:
			# Mop / Broom: reachable in front arc or right around feet
			var is_near_feet: bool = (horiz_dist < 1.5 and height_diff < 1.8 and aim_dot > -0.1)
			var is_aimed: bool = (aim_dot > 0.35 and dist_cam < max_reach)
			if is_near_feet or is_aimed:
				can_clean_this_spot = true
		
		if can_clean_this_spot:
			# Pick the single best target (highest aim alignment, closest distance)
			var score: float = aim_dot * 3.0 - (dist_cam * 1.0)
			if score > best_score:
				best_score = score
				best_spot = spot

	# Requirement 1: Only clean ONE spot at a time
	if best_spot and is_instance_valid(best_spot):
		best_spot.apply_cleaning(active_tool, delta * cleaning_rate)

func _physics_process(delta: float) -> void:
	if not is_active:
		rotation.x = lerp(rotation.x, original_rot.x, delta * 5.0)
		rotation.z = lerp(rotation.z, original_rot.z, delta * 5.0)
	# Idle sway
	var t = Time.get_ticks_msec() * 0.001
	position.x = lerp(position.x, sin(t * 0.8) * 0.008, delta * 2.0)
	is_active = false

func activate() -> void:
	show()

func deactivate() -> void:
	hide()
