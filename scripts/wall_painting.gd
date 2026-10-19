extends RigidBody3D
# Breakable Wall Painting that hangs securely on the wall until hit or knocked down

@export var object_name: String = "Wall Painting"
@export var dollar_value: float = 450.0
@export var is_hung: bool = true
@export var is_broken: bool = false

var impact_cooldown: float = 0.0

func _ready() -> void:
	add_to_group("interactable")
	add_to_group("breakable")
	add_to_group("painting")
	contact_monitor = true
	max_contacts_reported = 4
	body_entered.connect(_on_body_entered)
	
	# Start securely hung on the wall (kinematic freeze)
	freeze = true
	freeze_mode = FREEZE_MODE_KINEMATIC

func get_interaction_text() -> String:
	if is_broken:
		return ""
	if is_hung:
		return "[E] Nudge Painting"
	return ""

func interact(player: Node) -> void:
	if is_broken or not is_hung:
		return
	_unhang(Vector3(0, 0.2, 0.8))

func hit_by_tool(tool_name: String, hit_pos: Vector3 = Vector3.ZERO) -> void:
	if is_broken:
		return
	if is_hung:
		_unhang(Vector3(randf_range(-0.5, 0.5), 0.5, 1.5))
	else:
		_break_painting()

func hit_by_player(impulse: Vector3, is_sprinting: bool) -> void:
	if is_broken:
		return
	if is_hung:
		_unhang(impulse * 0.5 + Vector3(0, 0.2, 0.5))

func _unhang(push_impulse: Vector3 = Vector3.ZERO) -> void:
	if not is_hung:
		return
	is_hung = false
	freeze = false
	freeze_mode = FREEZE_MODE_STATIC
	linear_velocity = Vector3.ZERO
	angular_velocity = Vector3.ZERO
	apply_central_impulse(push_impulse)
	apply_torque_impulse(Vector3(randf_range(-1.0, 1.0), 0, randf_range(-1.0, 1.0)))
	ProceduralAudio.play_clatter(self)

func _on_body_entered(body: Node) -> void:
	if is_broken or is_hung:
		return
	# Smashes when hitting floor from the wall
	if linear_velocity.length() > 2.0 or not is_hung:
		_break_painting()

func _break_painting() -> void:
	if is_broken:
		return
	is_broken = true
	is_hung = false
	freeze = true

	GameManager.register_damage(object_name)
	ProceduralAudio.play_glass_break(self)
	_show_popup("MASTERPIECE RUINED! -$450")

	# Darken and splinter
	for child in get_children():
		if child is MeshInstance3D:
			var mat = StandardMaterial3D.new()
			mat.albedo_color = Color(0.25, 0.20, 0.18)
			child.set_surface_override_material(0, mat)
			child.scale = child.scale * Vector3(1.1, 0.2, 1.1)

	_spawn_debris()

	var t = get_tree().create_tween()
	t.tween_interval(3.0)
	t.tween_property(self, "scale", Vector3.ZERO, 0.5)
	t.tween_callback(queue_free)

func _show_popup(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.25, 0.15)
	l.font_size = 64
	l.outline_size = 12
	l.outline_modulate = Color(0, 0, 0, 0.95)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	get_parent().add_child(l)
	l.global_position = global_position + Vector3(0, 0.5, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "global_position", global_position + Vector3(0, 1.8, 0), 1.3)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.3)
	t.tween_callback(l.queue_free)

func _spawn_debris() -> void:
	for i in range(6):
		var d = RigidBody3D.new()
		d.mass = 0.1
		var mi = MeshInstance3D.new()
		var bm = BoxMesh.new()
		bm.size = Vector3(randf_range(0.1, 0.25), 0.04, randf_range(0.1, 0.25))
		mi.mesh = bm
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(0.45, 0.28, 0.15)
		mi.set_surface_override_material(0, mat)
		d.add_child(mi)
		
		var col = CollisionShape3D.new()
		var cs = BoxShape3D.new()
		cs.size = bm.size
		col.shape = cs
		d.add_child(col)
		
		get_parent().add_child(d)
		d.global_position = global_position + Vector3(randf_range(-0.3, 0.3), 0.1, randf_range(-0.1, 0.1))
		d.apply_central_impulse(Vector3(randf_range(-2.0, 2.0), randf_range(1.5, 3.5), randf_range(1.0, 3.0)))
		
		var t = d.get_tree().create_tween()
		t.tween_interval(4.0)
		t.tween_property(d, "scale", Vector3.ZERO, 0.4)
		t.tween_callback(d.queue_free)
