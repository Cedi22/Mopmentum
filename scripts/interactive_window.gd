extends StaticBody3D
# Interactive & breakable glass window / sliding patio door

@export var is_door: bool = true
@export var is_open: bool = false
@export var is_broken: bool = false
@export var dollar_value: float = 250.0

var closed_x: float = 0.0
var open_x: float = 0.0
var is_sliding: bool = false

@onready var mesh_instance: MeshInstance3D = $Mesh if has_node("Mesh") else null
@onready var col_shape: CollisionShape3D = $Col if has_node("Col") else null

func _ready() -> void:
	add_to_group("interactable")
	add_to_group("breakable")
	add_to_group("window")
	
	closed_x = position.x
	if closed_x < 0.0:
		open_x = closed_x - 3.2 # Slide left into side wall
	else:
		open_x = closed_x + 3.2 # Slide right into side wall

func get_interaction_text() -> String:
	if is_broken:
		return ""
	if is_door:
		return "[E] Close Glass Door" if is_open else "[E] Slide Glass Door Open"
	return ""

func interact(player: Node) -> void:
	if is_broken or not is_door or is_sliding:
		return
	is_sliding = true
	is_open = not is_open
	var target_x = open_x if is_open else closed_x
	
	ProceduralAudio.play_clatter(self)
	var t = get_tree().create_tween()
	t.tween_property(self, "position:x", target_x, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	t.tween_callback(func(): is_sliding = false)

func hit_by_player(impulse: Vector3, is_sprinting: bool) -> void:
	if is_broken:
		return
	if is_sprinting or impulse.length() > 6.0:
		_break_window()

func hit_by_tool(tool_name: String, hit_pos: Vector3 = Vector3.ZERO) -> void:
	if is_broken:
		return
	_break_window()

func _break_window() -> void:
	if is_broken:
		return
	is_broken = true
	
	GameManager.register_damage("Patio Window")
	ProceduralAudio.play_glass_break(self)
	
	_show_popup("WINDOW SHATTERED! -$250")

	if col_shape:
		col_shape.set_deferred("disabled", true)
	if mesh_instance:
		mesh_instance.hide()
	set_deferred("collision_layer", 0)
	set_deferred("collision_mask", 0)

	_spawn_glass_shards()

	var t = get_tree().create_tween()
	t.tween_interval(3.0)
	t.tween_callback(queue_free)

func _show_popup(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.2, 0.15)
	l.font_size = 72
	l.outline_size = 14
	l.outline_modulate = Color(0, 0, 0, 0.95)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	get_parent().add_child(l)
	l.global_position = global_position + Vector3(0, 1.0, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "global_position", global_position + Vector3(0, 2.4, 0), 1.5)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.5)
	t.tween_callback(l.queue_free)

func _spawn_glass_shards() -> void:
	for i in range(16):
		var d = RigidBody3D.new()
		d.mass = 0.02
		# Shards must NOT push or fling player: collision_layer 0, mask 1 (floor/walls only)
		d.collision_layer = 0
		d.collision_mask = 1

		var mi = MeshInstance3D.new()
		var bm = BoxMesh.new()
		bm.size = Vector3(randf_range(0.06, 0.22), randf_range(0.06, 0.22), 0.02)
		mi.mesh = bm

		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(0.7, 0.9, 1.0, 0.5)
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mat.roughness = 0.1
		mi.set_surface_override_material(0, mat)
		d.add_child(mi)

		var col = CollisionShape3D.new()
		var cs = BoxShape3D.new()
		cs.size = bm.size
		col.shape = cs
		d.add_child(col)

		get_parent().add_child(d)
		d.global_position = global_position + Vector3(randf_range(-1.0, 1.0), randf_range(-0.6, 0.6), randf_range(-0.05, 0.05))
		d.apply_central_impulse(Vector3(randf_range(-1.5, 1.5), randf_range(0.5, 2.0), randf_range(0.5, 2.0)))

		var t = d.get_tree().create_tween()
		t.tween_interval(4.0)
		t.tween_property(d, "scale", Vector3.ZERO, 0.5)
		t.tween_callback(d.queue_free)
