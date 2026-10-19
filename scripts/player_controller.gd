extends CharacterBody3D
# Player Controller - Slippery, momentum-based movement with sprint, collisions, and buffs

@onready var camera_pivot: Node3D = $CameraPivot
@onready var camera: Camera3D = $CameraPivot/Camera3D
@onready var tool_holder: Node3D = $CameraPivot/Camera3D/ToolHolder
@onready var interact_ray: RayCast3D = $CameraPivot/Camera3D/InteractRay

const MOVE_SPEED: float = 4.5
const SPRINT_SPEED: float = 7.5
const ACCELERATION: float = 2.5
const FRICTION: float = 1.8
const GRAVITY: float = 9.8

var wobble_time: float = 0.0
var horizontal_velocity: Vector3 = Vector3.ZERO
var is_sprinting: bool = false
var footstep_timer: float = 0.0
var footstep_interval: float = 0.45

var mouse_sensitivity: float = 0.002
var camera_pitch: float = 0.0
const MAX_PITCH: float = 1.3
const MIN_PITCH: float = -1.3

var current_tool_node: Node3D = null
var is_using_tool: bool = false
var interact_cooldown: float = 0.0
var tilt_amount: float = 0.0
var current_tilt: float = 0.0

# Mushroom Buff / Debuff State
var active_buff_name: String = ""
var buff_duration: float = 0.0
var speed_multiplier: float = 1.0
var wobble_multiplier: float = 1.0
var invert_controls: bool = false
var clean_rate_multiplier: float = 1.0
var jump_force: float = 0.0

func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	add_to_group("player")

func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		var mx = -event.relative.x * mouse_sensitivity
		var my = -event.relative.y * mouse_sensitivity
		if invert_controls:
			mx = -mx
			my = -my
		rotate_y(mx)
		camera_pitch += my
		camera_pitch = clamp(camera_pitch, MIN_PITCH, MAX_PITCH)
		camera_pivot.rotation.x = camera_pitch

	if event.is_action_pressed("pause"):
		if GameManager.current_state == GameManager.GameState.PLAYING:
			GameManager.pause_game()
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		elif GameManager.current_state == GameManager.GameState.PAUSED:
			GameManager.resume_game()
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _physics_process(delta: float) -> void:
	if GameManager.current_state != GameManager.GameState.PLAYING:
		return
	
	_update_buffs(delta)
	_handle_gravity(delta)
	_handle_movement(delta)
	_handle_wobble(delta)
	_handle_tool_use(delta)
	_handle_interaction()
	_update_footsteps(delta)
	
	# Clamp velocity to prevent physics solver explosions or insane flings
	velocity.x = clampf(velocity.x, -14.0, 14.0)
	velocity.z = clampf(velocity.z, -14.0, 14.0)
	velocity.y = clampf(velocity.y, -25.0, 12.0)

	move_and_slide()
	_handle_physics_collisions()

	# World boundary & void fall recovery
	if global_position.y < -3.5:
		_recover_from_fall()

func _recover_from_fall() -> void:
	global_position = Vector3(0.0, 0.4, 2.0)
	velocity = Vector3.ZERO
	horizontal_velocity = Vector3.ZERO
	ProceduralAudio.play_clatter(self)
	_show_hud_toast("⚠️ Whoops! Fell off the map! Safely returned inside.")

func _update_buffs(delta: float) -> void:
	if buff_duration > 0:
		buff_duration -= delta
		if buff_duration <= 0:
			_clear_buffs()

func apply_mushroom_effect(effect_type: String, duration: float, title: String) -> void:
	_clear_buffs()
	active_buff_name = title
	buff_duration = duration

	match effect_type:
		"ZOOMIES":
			speed_multiplier = 1.85
			wobble_multiplier = 1.5
		"SUPER_SUDS":
			clean_rate_multiplier = 4.0
		"DRUNK_TRIP":
			wobble_multiplier = 3.8
			speed_multiplier = 1.15
		"INVERTED":
			invert_controls = true
			wobble_multiplier = 2.0
		"SLOTH":
			speed_multiplier = 0.55
		"BOUNCY":
			velocity.y = 8.0
			speed_multiplier = 1.3
		"CASH":
			GameManager.add_score(250.0)
			ProceduralAudio.play_score_tick(self)

	_show_hud_toast("🍄 " + title)

func _clear_buffs() -> void:
	active_buff_name = ""
	buff_duration = 0.0
	speed_multiplier = 1.0
	wobble_multiplier = 1.0
	invert_controls = false
	clean_rate_multiplier = 1.0

func _handle_gravity(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= GRAVITY * delta

func _handle_movement(delta: float) -> void:
	is_sprinting = Input.is_action_pressed("sprint") or Input.is_key_pressed(KEY_SHIFT)
	var base_speed = SPRINT_SPEED if is_sprinting else MOVE_SPEED
	var speed = base_speed * speed_multiplier
	
	var input_dir = Vector2.ZERO
	if Input.is_action_pressed("move_forward"): input_dir.y -= 1
	if Input.is_action_pressed("move_back"):    input_dir.y += 1
	if Input.is_action_pressed("move_left"):    input_dir.x -= 1
	if Input.is_action_pressed("move_right"):   input_dir.x += 1
	
	if invert_controls:
		input_dir = -input_dir

	if input_dir.length() > 1.0:
		input_dir = input_dir.normalized()
		
	var forward = -global_transform.basis.z
	var right = global_transform.basis.x
	var wish_dir = (forward * -input_dir.y + right * input_dir.x)
	wish_dir.y = 0.0
	
	var accel = ACCELERATION * (1.5 if is_sprinting else 1.0)
	if wish_dir.length() > 0.01:
		wish_dir = wish_dir.normalized()
		horizontal_velocity = horizontal_velocity.lerp(wish_dir * speed, accel * delta)
	else:
		horizontal_velocity = horizontal_velocity.lerp(Vector3.ZERO, FRICTION * delta)

	wobble_time += delta * 2.0 * wobble_multiplier
	var drunk_x = sin(wobble_time * 1.3) * (0.08 * wobble_multiplier)
	var drunk_z = cos(wobble_time * 0.9) * (0.06 * wobble_multiplier)
	velocity.x = horizontal_velocity.x + drunk_x
	velocity.z = horizontal_velocity.z + drunk_z
	
	tilt_amount = -horizontal_velocity.dot(global_transform.basis.x) * (0.04 * wobble_multiplier)
	current_tilt = lerp(current_tilt, tilt_amount, delta * 3.0)

func _handle_wobble(delta: float) -> void:
	var speed_factor = clamp(horizontal_velocity.length() / MOVE_SPEED, 0.0, 1.5)
	var bob_y = sin(wobble_time * 2.5 * speed_factor) * 0.04 * speed_factor
	var bob_x = cos(wobble_time * 1.25 * speed_factor) * 0.02 * speed_factor
	camera.position.y = lerp(camera.position.y, bob_y, delta * 8.0)
	camera.position.x = lerp(camera.position.x, bob_x, delta * 8.0)
	
	var target_fov = 85.0 if is_sprinting else 75.0
	if camera.fov != target_fov:
		camera.fov = lerp(camera.fov, target_fov, delta * 6.0)

	camera.rotation.z = lerp(camera.rotation.z, current_tilt, delta * 4.0)

func _handle_physics_collisions() -> void:
	# Transfer momentum & break fragile objects on contact
	for i in get_slide_collision_count():
		var col = get_slide_collision(i)
		var collider = col.get_collider()
		if collider == null:
			continue
		if collider is CollisionObject3D and collider.collision_layer == 0:
			continue
		if collider is RigidBody3D:
			var push_dir = -col.get_normal()
			push_dir.y = 0.08
			push_dir = push_dir.normalized()
			var current_speed = horizontal_velocity.length()
			var push_force = clampf((current_speed + 1.8) * 2.8, 1.0, 16.0)
			collider.apply_central_impulse(push_dir * push_force)
			if collider.has_method("hit_by_player"):
				collider.hit_by_player(push_dir * push_force, is_sprinting or current_speed > 4.5)
		elif collider and collider.has_method("hit_by_player"):
			collider.hit_by_player(horizontal_velocity, is_sprinting)

func _handle_tool_use(delta: float) -> void:
	if interact_cooldown > 0:
		interact_cooldown -= delta
	is_using_tool = Input.is_action_pressed("use_tool")
	
	if current_tool_node and is_using_tool:
		if current_tool_node.has_method("use_tool"):
			current_tool_node.use_tool(delta * clean_rate_multiplier)

	if Input.is_action_just_pressed("use_tool"):
		_check_tool_strike()

func _check_tool_strike() -> void:
	# Raycast forward to hit breakables/props within swinging reach
	var space_state = get_world_3d().direct_space_state
	var cam_pos = camera.global_position
	var end_pos = cam_pos - camera.global_transform.basis.z * 2.2
	var query = PhysicsRayQueryParameters3D.create(cam_pos, end_pos)
	query.exclude = [self]
	var result = space_state.intersect_ray(query)
	if result:
		var hit_collider = result.collider
		if hit_collider.has_method("hit_by_tool"):
			hit_collider.hit_by_tool(GameManager.current_tool, result.position)
		elif hit_collider is RigidBody3D:
			var strike_dir = -camera.global_transform.basis.z + Vector3.UP * 0.3
			hit_collider.apply_central_impulse(strike_dir.normalized() * 5.0 * hit_collider.mass)

func _handle_interaction() -> void:
	# Update HUD interaction prompt
	_update_interact_prompt()

	if Input.is_action_just_pressed("interact") and interact_cooldown <= 0:
		interact_cooldown = 0.3
		if interact_ray.is_colliding():
			var hit = interact_ray.get_collider()
			if hit and hit.has_method("interact"):
				hit.interact(self)
				ProceduralAudio.play_clatter(self)

	if Input.is_action_just_pressed("switch_tool"):
		_cycle_tool()

func _update_interact_prompt() -> void:
	var hud = get_tree().get_first_node_in_group("hud")
	if not hud:
		return
	var prompt_label = hud.find_child("InteractPrompt", true, false)
	if not prompt_label:
		return

	if interact_ray.is_colliding():
		var hit = interact_ray.get_collider()
		if hit and hit.has_method("get_interaction_text"):
			prompt_label.text = hit.get_interaction_text()
			prompt_label.show()
			return
		elif hit and hit.has_method("interact"):
			prompt_label.text = "[E] Interact"
			prompt_label.show()
			return

	prompt_label.hide()

func _cycle_tool() -> void:
	var tools_list = ["mop", "sponge", "broom", "spray"]
	var current_idx = tools_list.find(GameManager.current_tool)
	var next_idx = (current_idx + 1) % tools_list.size()
	GameManager.set_tool(tools_list[next_idx])

func _update_footsteps(delta: float) -> void:
	if is_on_floor() and horizontal_velocity.length() > 0.8:
		footstep_timer += delta
		var interval = footstep_interval * (0.65 if is_sprinting else 1.0)
		if footstep_timer >= interval:
			footstep_timer = 0.0
			ProceduralAudio.play_footstep(self)

func _show_hud_toast(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.85, 0.2)
	l.font_size = 72
	l.outline_size = 14
	l.outline_modulate = Color(0, 0, 0, 0.95)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	get_parent().add_child(l)
	l.global_position = global_position + Vector3(0, 2.2, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "global_position", global_position + Vector3(0, 3.2, 0), 2.0)
	t.parallel().tween_property(l, "modulate:a", 0.0, 2.0)
	t.tween_callback(l.queue_free)

func equip_tool(tool_node: Node3D) -> void:
	current_tool_node = tool_node

func get_look_target() -> Vector3:
	if interact_ray.is_colliding():
		return interact_ray.get_collision_point()
	return camera.global_position + camera.global_transform.basis.z * -2.5

func get_camera_forward() -> Vector3:
	return -camera.global_transform.basis.z
