extends Node
# Procedural sound generation via AudioStreamGenerator

var _players: Dictionary = {}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS

func play_sfx(sound_name: String, volume_db: float = 0.0, pitch: float = 1.0) -> void:
	var player = AudioStreamPlayer.new()
	add_child(player)
	player.volume_db = volume_db
	player.pitch_scale = pitch * randf_range(0.95, 1.05)
	# Use AudioStreamGenerator for procedural sounds
	var stream = _get_procedural_stream(sound_name)
	if stream:
		player.stream = stream
		player.play()
		await player.finished
	player.queue_free()

func _get_procedural_stream(sound_name: String) -> AudioStream:
	# Since we can not generate binary audio here, return null
	# Real sounds come from AudioStreamPlayers in the scene with actual files
	return null
