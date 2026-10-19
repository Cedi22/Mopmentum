extends RigidBody3D
# Interactive & breakable floor lamp with connected stem, base, shade, and light toggle

@export var object_name: String = "Floor Lamp"
@export var dollar_value: float = 180.0
@export var is_on: bool = true
@export var is_broken: bool = false
@export var break_threshold: float = 3.2

var is_tipped: bool = false
var impact_cooldown: float = 0.0

@onready var light_node: OmniLight3D = $LampLight if has_node("LampLight") else null

func _ready() -> void:
	add_to_group("interactable")
	add_to_group("breakable")
	add_to_group("lamp")
	contact_monitor = true
	max_contacts_reported = 4
	body_entered.connect(_on_body_entered)

func get_interaction_text() -> String:
	if is_broken:
		return ""
	return "[E] Turn Off Lamp" if is_on else "[E] Turn On Lamp"

func interact(player: Node) -> void:
	if is_broken:
		return
	is_on = not is_on
	if light_node:
		light_node.visible = is_on
	ProceduralAudio.play_score_tick(self)
	_show_popup("CLICK! Lamp " + ("ON" if is_on else "OFF"))

func _physics_process(delta: float) -> void:
	if is_broken:
		return
	if impact_cooldown > 0:
		impact_cooldown -= delta

	# Check if tipped past 45 degrees
	var up_dot = global_transform.basis.y.dot(Vector3.UP)
	if up_dot < 0.5 and not is_tipped:
		is_tipped = true
		_break_lamp()

func _on_body_entered(body: Node) -> void:
	if is_broken or impact_cooldown > 0:
		return
	impact_cooldown = 0.25
	var speed = body.velocity.length() if body is CharacterBody3D else linear_velocity.length()
	if speed > break_threshold:
		_break_lamp()
	elif speed > 1.5 and not is_tipped:
		_tip_lamp(body)

func _tip_lamp(body: Node) -> void:
	is_tipped = true
	ProceduralAudio.play_clatter(self)
	if body:
		var push = (global_position - body.global_position).normalized()
		apply_central_impulse(push * 4.0 + Vector3(0, 0.5, 0))
		apply_torque_impulse(Vector3(randf_range(-2.0, 2.0), 0, randf_range(-2.0, 2.0)))

func hit_by_tool(tool_name: String, hit_pos: Vector3 = Vector3.ZERO) -> void:
	if is_broken:
		return
	apply_central_impulse(Vector3(randf_range(-1.0, 1.0), 1.0, randf_range(-1.0, 1.0)) * 6.0)
	apply_torque_impulse(Vector3(randf_range(-4.0, 4.0), 0, randf_range(-4.0, 4.0)))
	_break_lamp()

func hit_by_player(impulse: Vector3, is_sprinting: bool) -> void:
	if is_broken:
		return
	apply_central_impulse(impulse * 2.0)
	if is_sprinting or impulse.length() > 5.0:
		_break_lamp()
	else:
		_tip_lamp(null)

func _break_lamp() -> void:
	if is_broken:
		return
	is_broken = true

	if light_node:
		light_node.visible = false

	GameManager.register_damage(object_name)
	ProceduralAudio.play_glass_break(self)
	_show_popup("LAMP SMASHED! -$180")

	for child in get_children():
		if child is MeshInstance3D:
			var mat = StandardMaterial3D.new()
			mat.albedo_color = Color(0.25, 0.22, 0.20)
			child.set_surface_override_material(0, mat)

	_spawn_debris()

	var t = get_tree().create_tween()
	t.tween_interval(3.5)
	t.tween_property(self, "scale", Vector3.ZERO, 0.4)
	t.tween_callback(queue_free)

func _show_popup(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.3, 0.15)
	l.font_size = 64
	l.outline_size = 12
	l.outline_modulate = Color(0, 0, 0, 0.95)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	get_parent().add_child(l)
	l.global_position = global_position + Vector3(0, 1.2, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "global_position", global_position + Vector3(0, 2.4, 0), 1.4)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.4)
	t.tween_callback(l.queue_free)

func _spawn_debris() -> void:
	for i in range(8):
		var d = RigidBody3D.new()
		d.mass = 0.1
		var mi = MeshInstance3D.new()
		var bm = BoxMesh.new()
		bm.size = Vector3(randf_range(0.06, 0.16), randf_range(0.06, 0.14), randf_range(0.06, 0.16))
		mi.mesh = bm
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(1.0, 0.9, 0.5) if i < 4 else Color(0.3, 0.25, 0.2)
		mi.set_surface_override_material(0, mat)
		d.add_child(mi)
		
		var col = CollisionShape3D.new()
		var cs = BoxShape3D.new()
		cs.size = bm.size
		col.shape = cs
		d.add_child(col)
		
		get_parent().add_child(d)
		d.global_position = global_position + Vector3(randf_range(-0.2, 0.2), 0.5, randf_range(-0.2, 0.2))
		d.apply_central_impulse(Vector3(randf_range(-2.5, 2.5), randf_range(2.0, 4.0), randf_range(-2.5, 2.5)))
		
		var t = d.get_tree().create_tween()
		t.tween_interval(4.0)
		t.tween_property(d, "scale", Vector3.ZERO, 0.4)
		t.tween_callback(d.queue_free)
