extends Node
# Sets up the level - dirt spots are placed inline in the scene
# This script just starts the game and can add extra dirt if needed

@export var auto_start: bool = true

func _ready() -> void:
	# Register dirt spots already placed in scene
	call_deferred("_init_level")

func _init_level() -> void:
	if auto_start:
		GameManager.start_game()
	# Dirt nodes placed in scene already call GameManager.register_dirt_spot()
	# via their _ready. We give one extra frame for all to register.
