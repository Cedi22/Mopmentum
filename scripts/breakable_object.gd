extends RigidBody3D
# Breakable furniture/decoration - can be knocked over, smashed, and destroyed

@export var object_name: String = "generic":
	set(val):
		object_name = val
		object_type = val

@export var object_type: String = "generic"

@export var dollar_value: float = 50.0:
	set(val):
		dollar_value = val
		break_value = val

@export var break_value: float = 50.0

@export var break_impulse_threshold: float = 2.5:
	set(val):
		break_impulse_threshold = val
		break_threshold = val

@export var break_threshold: float = 2.5
@export var is_fragile: bool = false

var is_broken: bool = false
var is_tipped: bool = false
var impact_cooldown: float = 0.0

func _ready() -> void:
	add_to_group("breakable")
	contact_monitor = true
	max_contacts_reported = 6
	body_entered.connect(_on_body_entered)
	
	# Determine fragility from name if not explicitly set
	var lower_name = (object_name if object_name != "generic" else object_type).to_lower()
	if "glass" in lower_name or "vase" in lower_name or "porcelain" in lower_name:
		is_fragile = true
		if break_threshold > 2.0:
			break_threshold = 1.5

func _physics_process(delta: float) -> void:
	if is_broken:
		return

	if impact_cooldown > 0:
		impact_cooldown -= delta

	# Check if object tipped over on its side
	var up_dot = global_transform.basis.y.dot(Vector3.UP)
	if up_dot < 0.45 and not is_tipped:
		is_tipped = true
		if is_fragile:
			_break_object()
		else:
			_tip_object(linear_velocity.length())

func _on_body_entered(body: Node) -> void:
	if is_broken or impact_cooldown > 0:
		return
	impact_cooldown = 0.25

	var impact_speed: float = 0.0
	if body is CharacterBody3D:
		impact_speed = body.velocity.length()
		# Player pushing directly into object
		var push_dir = (global_position - body.global_position).normalized()
		apply_central_impulse(push_dir * maxf(impact_speed, 2.0) * mass * 0.7)
	else:
		impact_speed = linear_velocity.length()

	var effective_threshold = break_threshold * (0.4 if is_fragile else 1.0)
	if impact_speed >= effective_threshold:
		_break_object()
	elif impact_speed > effective_threshold * 0.4 and not is_tipped:
		_tip_object(impact_speed)

func hit_by_player(impulse: Vector3, is_sprinting: bool) -> void:
	if is_broken:
		return
	apply_central_impulse(impulse)
	var speed = impulse.length() / maxf(mass, 0.5)
	if is_sprinting or is_fragile or speed > break_threshold:
		_break_object()
	elif not is_tipped:
		_tip_object(speed)

func hit_by_tool(tool_name: String, hit_pos: Vector3 = Vector3.ZERO) -> void:
	if is_broken:
		return
	var forward_push = Vector3(randf_range(-0.5, 0.5), 1.0, randf_range(-0.5, 0.5)).normalized()
	apply_central_impulse(forward_push * 4.5 * mass)
	apply_torque_impulse(Vector3(randf_range(-2.0, 2.0), randf_range(-2.0, 2.0), randf_range(-2.0, 2.0)))
	
	if is_fragile or tool_name in ["mop", "broom"]:
		_break_object()
	else:
		_tip_object(3.0)

func _tip_object(impact: float) -> void:
	if is_tipped or is_broken:
		return
	is_tipped = true
	ProceduralAudio.play_clatter(self)
	_show_popup("TILTED!")

func _break_object() -> void:
	if is_broken:
		return
	is_broken = true
	
	var final_name = object_name if object_name != "generic" else object_type
	GameManager.register_damage(final_name)
	ProceduralAudio.play_glass_break(self)
	_show_popup(_get_break_message())

	# Darken and splinter mesh to show destroyed state
	for child in get_children():
		if child is MeshInstance3D:
			var mat = StandardMaterial3D.new()
			mat.albedo_color = Color(0.25, 0.22, 0.20)
			mat.roughness = 0.95
			child.set_surface_override_material(0, mat)
			child.scale = child.scale * Vector3(1.1, 0.4, 1.1)

	_spawn_debris()
	
	# Disable collisions safely so player doesn't get pushed or teleported
	set_deferred("collision_layer", 0)
	set_deferred("collision_mask", 0)
	set_deferred("freeze", true)
	sleeping = true

	_spawn_debris()

	var t = get_tree().create_tween()
	t.tween_interval(3.0)
	t.tween_property(self, "scale", Vector3.ZERO, 0.5)
	t.tween_callback(queue_free)

func _get_break_message() -> String:
	var msgs = [
		"SHATTERED!",
		"That'll cost ya!",
		"Whoops!",
		"$-" + str(int(dollar_value)),
		"Classic.",
		"Bonk!",
		"Slippery!",
		"RIP Deposit!",
	]
	return msgs[randi() % msgs.size()]

func _show_popup(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.25, 0.15)
	l.font_size = 64
	l.outline_size = 12
	l.outline_modulate = Color(0, 0, 0, 0.9)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	get_parent().add_child(l)
	l.global_position = global_position + Vector3(0, 0.8, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "global_position", global_position + Vector3(0, 2.0, 0), 1.2)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.2)
	t.tween_callback(l.queue_free)

func _spawn_debris() -> void:
	for i in range(8):
		var d = RigidBody3D.new()
		d.mass = 0.04
		# Debris does NOT collide with player (layer 0); only collides with floor/walls (mask 1)
		d.collision_layer = 0
		d.collision_mask = 1
		
		var mi = MeshInstance3D.new()
		var bm = BoxMesh.new()
		bm.size = Vector3(randf_range(0.04, 0.10), randf_range(0.04, 0.08), randf_range(0.04, 0.10))
		mi.mesh = bm
		
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(randf_range(0.5, 0.85), randf_range(0.4, 0.7), randf_range(0.3, 0.6))
		mi.set_surface_override_material(0, mat)
		d.add_child(mi)
		
		var col = CollisionShape3D.new()
		var cs = BoxShape3D.new()
		cs.size = bm.size
		col.shape = cs
		d.add_child(col)
		
		get_parent().add_child(d)
		d.global_position = global_position + Vector3(randf_range(-0.15, 0.15), 0.15, randf_range(-0.15, 0.15))
		d.apply_central_impulse(Vector3(randf_range(-1.5, 1.5), randf_range(1.0, 2.5), randf_range(-1.5, 1.5)))
		
		var t = d.get_tree().create_tween()
		t.tween_interval(3.5)
		t.tween_property(d, "scale", Vector3.ZERO, 0.4)
		t.tween_callback(d.queue_free)
