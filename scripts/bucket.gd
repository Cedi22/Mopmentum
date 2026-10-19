extends RigidBody3D
# Bucket that can be knocked over and spill water/cleaning liquid

@export var water_amount: float = 1.0
@export var is_tipped: bool = false

@onready var water_mesh: MeshInstance3D = $WaterMesh if has_node("WaterMesh") else null
@onready var spill_particles: GPUParticles3D = $SpillParticles if has_node("SpillParticles") else null
@onready var splash_sound: AudioStreamPlayer3D = $SplashSound if has_node("SplashSound") else null

var spill_timer: float = 0.0

func _ready() -> void:
	add_to_group("interactable")
	contact_monitor = true
	max_contacts_reported = 4
	body_entered.connect(_on_body_entered)

func get_interaction_text() -> String:
	if is_tipped:
		return "[E] Right Bucket & Refill Water"
	return "[E] Rinse Mop (Soap Boost)"

func interact(player: Node) -> void:
	if is_tipped:
		is_tipped = false
		water_amount = 1.0
		rotation = Vector3.ZERO
		position.y += 0.15
		linear_velocity = Vector3.ZERO
		angular_velocity = Vector3.ZERO
		if water_mesh:
			water_mesh.show()
		ProceduralAudio.play_clatter(self)
		_show_popup("Bucket Restored!")
	else:
		ProceduralAudio.play_score_tick(self)
		if player and player.has_method("apply_mushroom_effect"):
			player.apply_mushroom_effect("SUPER_SUDS", 12.0, "SOAPY WATER BOOST! (4x Clean)")
		_show_popup("Squeaky Clean Soap!")

func _show_popup(msg: String) -> void:
	var l = Label3D.new()
	l.text = msg
	l.modulate = Color(0.2, 0.8, 1.0)
	l.font_size = 64
	l.outline_size = 10
	l.outline_modulate = Color(0, 0, 0, 0.9)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	add_child(l)
	l.position = Vector3(0, 0.8, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "position", Vector3(0, 1.8, 0), 1.2)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.2)
	t.tween_callback(l.queue_free)

func _on_body_entered(body: Node) -> void:
	if linear_velocity.length() > 3.0 or is_tipped:
		_spill()

func _physics_process(delta: float) -> void:
	# Check if tipped
	var up = global_transform.basis.y
	if up.dot(Vector3.UP) < 0.5 and not is_tipped and water_amount > 0:
		_spill()

func _spill() -> void:
	if is_tipped:
		return
	is_tipped = true
	water_amount = 0.0
	if splash_sound:
		splash_sound.play()
	if water_mesh:
		water_mesh.hide()
	if spill_particles:
		spill_particles.emitting = true
	# Create wet floor stain
	_create_wet_stain()
	# Funny message
	_show_spill_popup()

func _create_wet_stain() -> void:
	var stain = MeshInstance3D.new()
	var quad = QuadMesh.new()
	quad.size = Vector2(1.5, 1.5)
	stain.mesh = quad
	stain.rotation_degrees.x = -90
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.5, 0.6, 0.9, 0.7)
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_ALWAYS
	stain.set_surface_override_material(0, mat)
	get_parent().add_child(stain)
	stain.global_position = global_position
	stain.global_position.y = 0.01
	# Add as dirt spot
	var dirt = load("res://scenes/dirt_spot.tscn")
	if dirt:
		var d = dirt.instantiate()
		d.dirt_type = 4  # liquid
		get_parent().add_child(d)
		d.global_position = global_position
		d.global_position.y = 0.01

func _show_spill_popup() -> void:
	var messages = ["SPLASH!", "There goes the water.", "Welp.", "Clean that up too!"]
	var l = Label3D.new()
	l.text = messages[randi() % messages.size()]
	l.modulate = Color(0.3, 0.6, 1.0)
	l.font_size = 64
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(l)
	l.position = Vector3(0, 1.0, 0)
	var t = l.get_tree().create_tween()
	t.tween_property(l, "position", Vector3(0, 2.0, 0), 1.5)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.5)
	t.tween_callback(l.queue_free)
