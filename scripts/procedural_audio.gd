extends Node
# Generates procedural sound effects using AudioStreamGenerator
# Called by other nodes to play sounds without needing audio files

static func _get_safe_parent(parent: Node) -> Node:
	if parent and is_instance_valid(parent) and parent.is_inside_tree() and not parent.is_queued_for_deletion():
		return parent
	var main_loop = Engine.get_main_loop()
	if main_loop and main_loop is SceneTree and main_loop.root:
		return main_loop.root
	return null

static func play_score_tick(parent: Node) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.25
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -6.0
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var tone1 = sin(t * 880.0 * TAU) * 0.25 * exp(-t * 10.0)
			var tone2 = sin(t * 1760.0 * TAU) * 0.15 * exp(-t * 16.0)
			pb.push_frame(Vector2(tone1 + tone2, tone1 + tone2))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.25)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()

static func play_squeak(parent: Node, pitch: float = 1.0) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.1
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -8.0
	p.pitch_scale = pitch
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var freq = 800.0 + 400.0 * sin(t * 20.0)
			var sample = sin(t * freq * TAU) * 0.3 * exp(-t * 15.0)
			pb.push_frame(Vector2(sample, sample))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.15)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()

static func play_clatter(parent: Node) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.3
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -5.0
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var noise = randf_range(-1.0, 1.0) * 0.5 * exp(-t * 8.0)
			var ring = sin(t * 1200.0 * TAU) * 0.2 * exp(-t * 12.0)
			pb.push_frame(Vector2(noise + ring, noise + ring))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.35)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()

static func play_splash(parent: Node) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.5
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -4.0
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var noise = randf_range(-1.0, 1.0) * exp(-t * 5.0)
			var low = sin(t * 200.0 * TAU) * 0.3 * exp(-t * 6.0)
			pb.push_frame(Vector2((noise + low) * 0.6, (noise + low) * 0.6))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.55)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()

static func play_glass_break(parent: Node) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.6
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -2.0
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var noise = randf_range(-1.0, 1.0) * 0.8 * exp(-t * 4.0)
			var high = sin(t * 3000.0 * TAU) * 0.2 * exp(-t * 10.0)
			var mid = sin(t * 1500.0 * TAU) * 0.15 * exp(-t * 7.0)
			pb.push_frame(Vector2(noise + high + mid, noise + high + mid))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.65)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()

static func play_footstep(parent: Node) -> void:
	var target = _get_safe_parent(parent)
	if not target:
		return
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.15
	var p = AudioStreamPlayer.new()
	target.add_child(p)
	p.stream = gen
	p.volume_db = -12.0
	p.pitch_scale = randf_range(0.9, 1.1)
	p.play()
	var pb: AudioStreamGeneratorPlayback = p.get_stream_playback()
	if pb:
		var frames = pb.get_frames_available()
		for i in range(frames):
			var t = float(i) / gen.mix_rate
			var thump = randf_range(-1.0, 1.0) * exp(-t * 25.0) * 0.6
			var click = sin(t * 500.0 * TAU) * 0.2 * exp(-t * 40.0)
			pb.push_frame(Vector2(thump + click, thump + click))
	var tree = target.get_tree()
	if tree:
		var timer = tree.create_timer(0.2)
		await timer.timeout
	if is_instance_valid(p):
		p.queue_free()
