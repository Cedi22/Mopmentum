extends CanvasLayer

@onready var reason_label: Label = $Panel/VBox/ReasonLabel
@onready var score_label: Label = $Panel/VBox/ScoreLabel
@onready var restart_btn: Button = $Panel/VBox/RestartButton
@onready var menu_btn: Button = $Panel/VBox/MenuButton
@onready var panel: Panel = $Panel

const GAME_OVER_REASONS = {
	"time_up": "⏰ Time's Up!\nYou ran out of time. The house remains filthy.",
	"too_much_damage": "💸 BANKRUPTCY!\nYou destroyed $2000 worth of property.\nYou're fired. Again.",
}

func _ready() -> void:
	GameManager.game_over.connect(_on_game_over)
	GameManager.level_complete.connect(_on_level_complete)
	restart_btn.pressed.connect(_on_restart)
	menu_btn.pressed.connect(_on_menu)
	visible = false
	process_mode = Node.PROCESS_MODE_ALWAYS
	# Style buttons
	_style_button(restart_btn, Color(0.2, 0.6, 1.0))
	_style_button(menu_btn, Color(0.35, 0.3, 0.45))
	# Style panel
	_style_panel()

func _style_panel() -> void:
	if not panel:
		return
	var style = StyleBoxFlat.new()
	style.bg_color = Color(0.08, 0.08, 0.12, 0.95)
	style.corner_radius_top_left = 16
	style.corner_radius_top_right = 16
	style.corner_radius_bottom_left = 16
	style.corner_radius_bottom_right = 16
	style.border_width_top = 3
	style.border_color = Color(0.3, 0.5, 1.0, 0.5)
	style.content_margin_left = 30
	style.content_margin_right = 30
	style.content_margin_top = 20
	style.content_margin_bottom = 20
	panel.add_theme_stylebox_override("panel", style)

func _style_button(btn: Button, color: Color) -> void:
	var style = StyleBoxFlat.new()
	style.bg_color = color
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	style.content_margin_left = 16
	style.content_margin_right = 16
	style.content_margin_top = 8
	style.content_margin_bottom = 8
	btn.add_theme_stylebox_override("normal", style)
	var hover = style.duplicate()
	hover.bg_color = color.lightened(0.15)
	btn.add_theme_stylebox_override("hover", hover)
	var pressed = style.duplicate()
	pressed.bg_color = color.darkened(0.2)
	btn.add_theme_stylebox_override("pressed", pressed)
	btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())

func _on_game_over(reason: String) -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	if reason_label:
		reason_label.text = GAME_OVER_REASONS.get(reason, "Something went wrong.\n(That's kind of on you.)")
	if score_label:
		score_label.text = "Cleanliness: %d%%\nDamage: $%.0f" % [
			int(GameManager.cleanliness_percent),
			GameManager.total_damage_cost
		]
	_animate_in()

func _on_level_complete(stats: Dictionary) -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var grade = _get_grade(stats.score)
	if reason_label:
		reason_label.text = "✨ HOUSE CLEAN! ✨\nGrade: %s" % grade
		reason_label.modulate = Color(0.3, 1.0, 0.5)
	if score_label:
		score_label.text = "Score: %.0f\nCleanliness: %d%%\nDamage: $%.0f\nTime: %s" % [
			stats.score,
			int(stats.cleanliness),
			stats.damage_cost,
			GameManager.format_time(stats.time)
		]
	_animate_in()

func _animate_in() -> void:
	if panel:
		panel.modulate.a = 0.0
		panel.scale = Vector2(0.9, 0.9)
		var t = get_tree().create_tween()
		t.tween_property(panel, "modulate:a", 1.0, 0.4)
		t.parallel().tween_property(panel, "scale", Vector2(1.0, 1.0), 0.3).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)

func _get_grade(score: float) -> String:
	if score >= 9000: return "S — SPOTLESS ✨"
	elif score >= 7000: return "A — Gleaming"
	elif score >= 5000: return "B — Decent"
	elif score >= 3000: return "C — Mediocre"
	elif score >= 1000: return "D — Questionable"
	else: return "F — You Call This Clean?"

func _on_restart() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://levels/level_01.tscn")

func _on_menu() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
