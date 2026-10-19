extends Node3D
# Visible dirt spots: Distinct 3D trash piles for broom, muddy brown floor for mop, table grime for sponge

signal cleaned

enum DirtType { GENERIC, STAIN, DUST, MUD, LIQUID }

@export var dirt_type: DirtType = DirtType.GENERIC
@export var clean_time_required: float = 1.5

var clean_progress: float = 0.0
var is_cleaned: bool = false
var dirt_mesh: MeshInstance3D = null

# 3D Trash Pile for Broom
var trash_pile_root: Node3D = null
var trash_pieces: Array[Node3D] = []

# 3D Tool UI Indicator Nodes
var indicator_root: Node3D = null
var badge_sprite: Sprite3D = null
var tool_label: Label3D = null
var progress_bar_3d: Label3D = null

# Progress tracked separately per tool so progress cannot be shared or continued by wrong tools!
var tool_progress: Dictionary = {
	"mop": 0.0,
	"sponge": 0.0,
	"broom": 0.0,
	"spray": 0.0,
}

const REQUIRED_TOOL = {
	DirtType.GENERIC: "mop",
	DirtType.STAIN:   "sponge",   # Tables, counters, chairs, bookshelf
	DirtType.DUST:    "broom",    # 3D trash & debris piles
	DirtType.MUD:     "mop",      # Floor mud puddles
	DirtType.LIQUID:  "mop",      # Liquid spills
}

const PRIMARY_TOOL = REQUIRED_TOOL

const TEXTURE_PATHS = {
	DirtType.GENERIC: "res://assets/textures/dirt_mud_splat.png",
	DirtType.STAIN:   "res://assets/textures/dirt_table_grime.png",
	DirtType.DUST:    "res://assets/textures/dirt_dust_cluster.png",
	DirtType.MUD:     "res://assets/textures/dirt_mud_splat.png",
	DirtType.LIQUID:  "res://assets/textures/dirt_coffee_spill.png",
}

const BADGE_PATHS = {
	"mop":    "res://assets/textures/badge_mop.png",
	"broom":  "res://assets/textures/badge_broom.png",
	"sponge": "res://assets/textures/badge_sponge.png",
	"spray":  "res://assets/textures/badge_spray.png",
}

const DIRT_CLEAN_TIMES = {
	DirtType.GENERIC: 1.8,
	DirtType.STAIN:   2.0,   # Snappy table sponge scrubbing
	DirtType.DUST:    1.6,   # Snappy 3D trash sweeping
	DirtType.MUD:     1.8,   # Snappy floor mud mopping
	DirtType.LIQUID:  1.5,   # Snappy liquid spill mopping
}

func _ready() -> void:
	add_to_group("dirt_spot")
	clean_time_required = DIRT_CLEAN_TIMES.get(dirt_type, 1.8)
	
	# Locate existing mesh or create quad
	for child in get_children():
		if child is MeshInstance3D and child.name != "BadgeSprite":
			dirt_mesh = child
			break
	
	if not dirt_mesh:
		dirt_mesh = MeshInstance3D.new()
		var q = QuadMesh.new()
		q.size = Vector2(0.9, 0.9)
		dirt_mesh.mesh = q
		dirt_mesh.rotation_degrees.x = -90
		add_child(dirt_mesh)

	_setup_dirt_visuals()
	_setup_indicator_badge()
	GameManager.register_dirt_spot()
	call_deferred("_snap_to_surface")

func _snap_to_surface() -> void:
	if not is_inside_tree():
		return
	var space_state = get_world_3d().direct_space_state
	# Cast downward to detect tables, counters, chairs, or floors
	var from_pos = global_position + Vector3(0, 0.35, 0)
	var to_pos = global_position + Vector3(0, -1.2, 0)
	var query = PhysicsRayQueryParameters3D.create(from_pos, to_pos)
	query.collide_with_areas = false
	query.collide_with_bodies = true
	var result = space_state.intersect_ray(query)
	if result:
		# Place 3mm above surface to prevent any depth clipping or floating
		global_position.y = result.position.y + 0.003
	elif global_position.y > 0.05 and global_position.y < 0.3:
		# Fallback to floor level if placed slightly above floor
		global_position.y = 0.004

func _setup_dirt_visuals() -> void:
	var tex_path = TEXTURE_PATHS.get(dirt_type, "res://assets/textures/dirt_mud_splat.png")
	var tex = load(tex_path)
	
	var mat = StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_MIX
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
	mat.render_priority = 2 # Render cleanly on top of tables, chairs, and floors

	if tex:
		mat.albedo_texture = tex
		mat.albedo_color = Color(1.0, 1.0, 1.0, 1.0) # Full brightness and contrast
		if dirt_type == DirtType.MUD:
			mat.roughness = 0.3
		elif dirt_type == DirtType.STAIN:
			mat.roughness = 0.4
		elif dirt_type == DirtType.LIQUID:
			mat.roughness = 0.1
		else:
			mat.roughness = 0.6
	else:
		mat.albedo_color = Color(0.35, 0.22, 0.12, 0.95)

	dirt_mesh.set_surface_override_material(0, mat)

	# If this is DUST (Broom): Build a distinct 3D Trash Pile!
	if dirt_type == DirtType.DUST:
		_build_3d_trash_pile()

func _build_3d_trash_pile() -> void:
	trash_pile_root = Node3D.new()
	add_child(trash_pile_root)

	# 1. Crumpled Paper Wad 1 (White paper ball)
	var paper1 = MeshInstance3D.new()
	var bm1 = BoxMesh.new()
	bm1.size = Vector3(0.09, 0.08, 0.09)
	paper1.mesh = bm1
	paper1.position = Vector3(-0.08, 0.04, 0.05)
	paper1.rotation_degrees = Vector3(25, 45, 15)
	var p1_mat = StandardMaterial3D.new()
	p1_mat.albedo_color = Color(0.95, 0.94, 0.92)
	p1_mat.roughness = 0.9
	paper1.set_surface_override_material(0, p1_mat)
	trash_pile_root.add_child(paper1)
	trash_pieces.append(paper1)

	# 2. Crumpled Kraft Paper Wad 2 (Brown cardboard ball)
	var paper2 = MeshInstance3D.new()
	var bm2 = BoxMesh.new()
	bm2.size = Vector3(0.08, 0.07, 0.08)
	paper2.mesh = bm2
	paper2.position = Vector3(0.07, 0.035, -0.06)
	paper2.rotation_degrees = Vector3(-35, 15, -45)
	var p2_mat = StandardMaterial3D.new()
	p2_mat.albedo_color = Color(0.72, 0.54, 0.35)
	p2_mat.roughness = 0.95
	paper2.set_surface_override_material(0, p2_mat)
	trash_pile_root.add_child(paper2)
	trash_pieces.append(paper2)

	# 3. Crushed Tin Soda Can (Red/Silver cylinder on its side)
	var can = MeshInstance3D.new()
	var cm = CylinderMesh.new()
	cm.top_radius = 0.038
	cm.bottom_radius = 0.038
	cm.height = 0.12
	cm.radial_segments = 8
	can.mesh = cm
	can.position = Vector3(0.02, 0.04, 0.08)
	can.rotation_degrees = Vector3(0, 30, 85) # lying on side
	var can_mat = StandardMaterial3D.new()
	can_mat.albedo_color = Color(0.85, 0.18, 0.15)
	can_mat.metallic = 0.8
	can_mat.roughness = 0.3
	can.set_surface_override_material(0, can_mat)
	trash_pile_root.add_child(can)
	trash_pieces.append(can)

	# 4. Yellow Snack Wrapper
	var wrap = MeshInstance3D.new()
	var wm = BoxMesh.new()
	wm.size = Vector3(0.11, 0.015, 0.06)
	wrap.mesh = wm
	wrap.position = Vector3(-0.06, 0.01, -0.08)
	wrap.rotation_degrees = Vector3(10, -60, 5)
	var w_mat = StandardMaterial3D.new()
	w_mat.albedo_color = Color(0.95, 0.82, 0.10)
	w_mat.roughness = 0.4
	wrap.set_surface_override_material(0, w_mat)
	trash_pile_root.add_child(wrap)
	trash_pieces.append(wrap)

	# 5. Dust / Lint fluff sphere
	var fluff = MeshInstance3D.new()
	var sm = SphereMesh.new()
	sm.radius = 0.06
	sm.height = 0.08
	fluff.mesh = sm
	fluff.position = Vector3(0.0, 0.03, 0.0)
	var f_mat = StandardMaterial3D.new()
	f_mat.albedo_color = Color(0.60, 0.60, 0.65, 0.85)
	f_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	f_mat.roughness = 1.0
	fluff.set_surface_override_material(0, f_mat)
	trash_pile_root.add_child(fluff)
	trash_pieces.append(fluff)

func _setup_indicator_badge() -> void:
	indicator_root = Node3D.new()
	indicator_root.position = Vector3(0, 0.45, 0)
	add_child(indicator_root)

	var prim_tool = PRIMARY_TOOL.get(dirt_type, "mop")
	var badge_tex_path = BADGE_PATHS.get(prim_tool, "res://assets/textures/badge_mop.png")
	var b_tex = load(badge_tex_path)

	# Floating Circular Tool Badge
	badge_sprite = Sprite3D.new()
	badge_sprite.texture = b_tex
	badge_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	badge_sprite.pixel_size = 0.0011
	badge_sprite.modulate.a = 0.0
	indicator_root.add_child(badge_sprite)

	# Tool Advice Label
	tool_label = Label3D.new()
	tool_label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	tool_label.position = Vector3(0, 0.20, 0)
	tool_label.font_size = 30
	tool_label.outline_size = 8
	tool_label.outline_modulate = Color(0, 0, 0, 0.9)
	tool_label.text = prim_tool.to_upper()
	tool_label.modulate = Color(1.0, 0.9, 0.4, 0.0)
	indicator_root.add_child(tool_label)

	# Clean Progress Bar Label
	progress_bar_3d = Label3D.new()
	progress_bar_3d.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	progress_bar_3d.position = Vector3(0, -0.18, 0)
	progress_bar_3d.font_size = 28
	progress_bar_3d.outline_size = 6
	progress_bar_3d.outline_modulate = Color(0, 0, 0, 0.9)
	progress_bar_3d.text = ""
	progress_bar_3d.modulate = Color(0.2, 1.0, 0.5, 0.0)
	indicator_root.add_child(progress_bar_3d)

func _process(delta: float) -> void:
	if is_cleaned or not is_inside_tree():
		return

	# Badge bobbing
	var time_now = Time.get_ticks_msec() * 0.001
	if indicator_root:
		indicator_root.position.y = 0.45 + sin(time_now * 2.5 + global_position.x) * 0.04

	# Check distance to player camera for proximity fade
	var player = get_tree().get_first_node_in_group("player")
	if not player:
		return

	var cam = player.get_node_or_null("CameraPivot/Camera3D")
	var cam_pos = cam.global_position if cam else player.global_position
	var dist = cam_pos.distance_to(global_position)
	
	# Fade in when within 4.0 meters
	var target_alpha: float = clampf(inverse_lerp(4.5, 2.2, dist), 0.0, 1.0)
	
	var current_tool = GameManager.current_tool.to_lower()
	var req_tool = get_required_tool().to_lower()
	var is_correct = (current_tool == req_tool)

	var tool_keys = {
		"mop": "1",
		"sponge": "2",
		"broom": "3",
		"spray": "4",
	}
	var key_hint = tool_keys.get(req_tool, "1")

	if is_correct:
		tool_label.text = "USE " + req_tool.to_upper() + " [LMB]"
		tool_label.modulate = Color(0.25, 1.0, 0.45, target_alpha)
		badge_sprite.modulate = Color(1.0, 1.0, 1.0, target_alpha)

		# Only display clean progress for THIS tool!
		var p = tool_progress.get(req_tool, 0.0)
		if p > 0.01:
			progress_bar_3d.text = "%d%% Cleaned" % int(p * 100)
			progress_bar_3d.modulate = Color(0.2, 1.0, 0.5, target_alpha)
		else:
			progress_bar_3d.text = ""
	else:
		tool_label.text = "REQUIRES " + req_tool.to_upper() + " [Key " + key_hint + "]\n(" + current_tool.to_upper() + " CANNOT CLEAN THIS)"
		tool_label.modulate = Color(1.0, 0.35, 0.25, target_alpha)
		badge_sprite.modulate = Color(1.0, 0.5, 0.4, target_alpha * 0.95)
		# Crucial: hide progress completely when holding the wrong tool!
		progress_bar_3d.text = ""

func get_required_tool() -> String:
	return REQUIRED_TOOL.get(dirt_type, "mop")

func can_clean_with(tool_name: String) -> bool:
	if is_cleaned:
		return false
	# Strictly limited to the actual tool needed!
	return tool_name.to_lower() == get_required_tool().to_lower()

func apply_cleaning(tool_name: String, delta: float) -> void:
	if is_cleaned:
		return
	var req_tool = get_required_tool().to_lower()
	if tool_name.to_lower() != req_tool:
		# Cannot clean or progress with any other tool!
		return

	tool_progress[req_tool] += delta / clean_time_required
	tool_progress[req_tool] = min(tool_progress[req_tool], 1.0)
	clean_progress = tool_progress[req_tool]
	
	_update_appearance()
	
	# If sweeping trash with broom, scatter and shrink trash pieces
	if trash_pile_root and trash_pieces.size() > 0:
		var rem_scale = maxf(1.0 - clean_progress, 0.01)
		for piece in trash_pieces:
			if is_instance_valid(piece):
				piece.scale = Vector3(rem_scale, rem_scale, rem_scale)
				piece.rotation.y += delta * 4.0

	if clean_progress >= 1.0:
		_complete_clean()

func _update_appearance() -> void:
	if dirt_mesh:
		var mat = dirt_mesh.get_surface_override_material(0)
		if mat:
			var alpha = (1.0 - clean_progress) * 0.95
			mat.albedo_color.a = alpha

func _complete_clean() -> void:
	if is_cleaned:
		return
	is_cleaned = true
	cleaned.emit()
	GameManager.clean_dirt_spot()
	
	if indicator_root:
		indicator_root.hide()

	# Scatter remaining trash outward
	if trash_pile_root:
		for piece in trash_pieces:
			if is_instance_valid(piece):
				var t_piece = piece.get_tree().create_tween()
				t_piece.tween_property(piece, "scale", Vector3.ZERO, 0.2)

	var t = get_tree().create_tween()
	t.tween_property(self, "scale", Vector3(0.01, 0.01, 0.01), 0.25)
	t.tween_callback(queue_free)
