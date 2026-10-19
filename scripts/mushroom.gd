extends StaticBody3D
# Interactive Mushroom that grants random buffs and debuffs when consumed or whacked

@export var mushroom_type: String = "red"
var is_consumed: bool = false

const RED_EFFECTS = [
	{"type": "ZOOMIES",    "duration": 15.0, "title": "CAFFEINE ZOOMIES! (1.8x Speed)"},
	{"type": "SUPER_SUDS", "duration": 15.0, "title": "SUPER SUDS! (4x Clean Power)"},
	{"type": "BOUNCY",     "duration": 10.0, "title": "SUPER BOUNCE! (Air Time)"},
	{"type": "CASH",       "duration": 0.0,  "title": "GOLDEN SPORES! (+$250 Bonus)"},
]

const BLUE_EFFECTS = [
	{"type": "DRUNK_TRIP", "duration": 12.0, "title": "PSYCHEDELIC WOBBLE! (Drunk Vision)"},
	{"type": "INVERTED",   "duration": 8.0,  "title": "INVERTED BRAIN! (Controls Swapped)"},
	{"type": "SUPER_SUDS", "duration": 15.0, "title": "MYSTIC CLEANSE! (4x Clean Power)"},
	{"type": "SLOTH",      "duration": 10.0, "title": "MOLASSES SPORES! (Slow Mo)"},
]

func _ready() -> void:
	add_to_group("interactable")
	add_to_group("mushroom")

func get_interaction_text() -> String:
	if is_consumed:
		return ""
	var col = "Red" if mushroom_type == "red" else "Blue"
	return "[E] Eat " + col + " Mushroom"

func interact(player: Node) -> void:
	if is_consumed:
		return
	_consume(player)

func hit_by_tool(tool_name: String, hit_pos: Vector3 = Vector3.ZERO) -> void:
	if is_consumed:
		return
	var player = get_tree().get_first_node_in_group("player")
	if player:
		_consume(player)

func hit_by_player(impulse: Vector3, is_sprinting: bool) -> void:
	if is_consumed:
		return
	if is_sprinting:
		var player = get_tree().get_first_node_in_group("player")
		if player:
			_consume(player)

func _consume(player: Node) -> void:
	if is_consumed:
		return
	is_consumed = true
	collision_layer = 0
	collision_mask = 0

	var pool = RED_EFFECTS if mushroom_type == "red" else BLUE_EFFECTS
	var selected = pool[randi() % pool.size()]

	if player and player.has_method("apply_mushroom_effect"):
		player.apply_mushroom_effect(selected["type"], selected["duration"], selected["title"])

	ProceduralAudio.play_score_tick(player if player else self)
	_spawn_spores()

	var t = get_tree().create_tween()
	t.tween_property(self, "scale", Vector3(1.3, 1.3, 1.3), 0.1)
	t.tween_property(self, "scale", Vector3.ZERO, 0.2)
	t.tween_callback(queue_free)

func _spawn_spores() -> void:
	var color = Color(1.0, 0.2, 0.2) if mushroom_type == "red" else Color(0.2, 0.6, 1.0)
	for i in range(12):
		var p = MeshInstance3D.new()
		var sm = SphereMesh.new()
		sm.radius = randf_range(0.04, 0.09)
		sm.height = sm.radius * 2.0
		p.mesh = sm
		
		var mat = StandardMaterial3D.new()
		mat.albedo_color = color
		mat.emission_enabled = true
		mat.emission = color
		mat.emission_energy_multiplier = 1.2
		p.set_surface_override_material(0, mat)
		
		get_parent().add_child(p)
		p.global_position = global_position + Vector3(0, 0.3, 0)
		
		var t = p.get_tree().create_tween()
		var dir = Vector3(randf_range(-1.0, 1.0), randf_range(0.5, 1.8), randf_range(-1.0, 1.0)).normalized()
		t.tween_property(p, "global_position", p.global_position + dir * randf_range(0.8, 1.6), 0.7)
		t.parallel().tween_property(p, "scale", Vector3.ZERO, 0.7)
		t.tween_callback(p.queue_free)
