extends Node

signal cleanliness_changed(value: float)
signal damage_changed(amount: float)
signal tool_changed(tool_name: String)
signal game_over(reason: String)
signal level_complete(stats: Dictionary)

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE }

var current_state: GameState = GameState.MENU
var score: float = 0.0
var current_score: float = 0.0
var total_damage_cost: float = 0.0
var cleanliness_percent: float = 0.0
var time_elapsed: float = 0.0
var time_limit: float = 300.0

func add_score(amount: float) -> void:
	score += amount
	current_score = score

var total_dirt_spots: int = 0
var cleaned_dirt_spots: int = 0
var broken_objects: int = 0
var current_tool: String = "mop"

const OBJECT_COSTS = {
	"vase": 250.0,
	"lamp": 180.0,
	"painting": 450.0,
	"chair": 120.0,
	"glass": 35.0,
	"plate": 25.0,
	"trophy": 300.0,
	"flowerpot": 60.0,
	"mirror": 200.0,
	"milk": 350.0,
	"caution_sign": 120.0,
	"barrel": 100.0,
	"mug": 45.0,
	"generic": 75.0,
}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS

func start_game() -> void:
	current_state = GameState.PLAYING
	score = 0.0
	total_damage_cost = 0.0
	time_elapsed = 0.0
	cleaned_dirt_spots = 0
	broken_objects = 0
	cleanliness_percent = 0.0
	var spots = get_tree().get_nodes_in_group("dirt_spot").size()
	if spots > 0:
		total_dirt_spots = spots
	damage_changed.emit(total_damage_cost)
	cleanliness_changed.emit(cleanliness_percent)

func _process(delta: float) -> void:
	if current_state == GameState.PLAYING:
		time_elapsed += delta
		if time_elapsed >= time_limit:
			trigger_game_over("time_up")

func register_dirt_spot() -> void:
	total_dirt_spots += 1

func clean_dirt_spot() -> void:
	cleaned_dirt_spots += 1
	_update_cleanliness()

func _update_cleanliness() -> void:
	var remaining_spots = get_tree().get_nodes_in_group("dirt_spot").size()
	var total = max(total_dirt_spots, remaining_spots + cleaned_dirt_spots)
	if total > 0:
		cleanliness_percent = clampf(float(cleaned_dirt_spots) / float(total) * 100.0, 0.0, 100.0)
	else:
		cleanliness_percent = 0.0
	cleanliness_changed.emit(cleanliness_percent)
	if cleanliness_percent >= 100.0 and cleaned_dirt_spots > 0:
		trigger_level_complete()

func register_damage(object_type: String) -> void:
	var cost = OBJECT_COSTS.get(object_type, 50.0)
	total_damage_cost += cost
	broken_objects += 1
	damage_changed.emit(total_damage_cost)
	if total_damage_cost >= 2000.0:
		trigger_game_over("too_much_damage")

func trigger_game_over(reason: String) -> void:
	if current_state == GameState.LEVEL_COMPLETE:
		return
	current_state = GameState.GAME_OVER
	game_over.emit(reason)

func trigger_level_complete() -> void:
	current_state = GameState.LEVEL_COMPLETE
	var final_score = _calculate_score()
	var stats = {
		"score": final_score,
		"cleanliness": cleanliness_percent,
		"damage_cost": total_damage_cost,
		"time": time_elapsed,
		"broken_objects": broken_objects,
	}
	level_complete.emit(stats)

func _calculate_score() -> float:
	var base = cleanliness_percent * 100.0
	var time_bonus = max(0.0, (time_limit - time_elapsed) * 5.0)
	var damage_penalty = total_damage_cost * 2.0
	return max(0.0, base + time_bonus - damage_penalty)

func set_tool(tool_name: String) -> void:
	current_tool = tool_name
	tool_changed.emit(tool_name)

func get_time_remaining() -> float:
	return max(0.0, time_limit - time_elapsed)

func format_time(seconds: float) -> String:
	var mins = int(seconds) / 60
	var secs = int(seconds) % 60
	return "%02d:%02d" % [mins, secs]

func pause_game() -> void:
	if current_state == GameState.PLAYING:
		current_state = GameState.PAUSED
		get_tree().paused = true

func resume_game() -> void:
	if current_state == GameState.PAUSED:
		current_state = GameState.PLAYING
		get_tree().paused = false
