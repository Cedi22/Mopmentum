extends CanvasLayer

@onready var resume_btn: Button = $Panel/VBox/ResumeButton
@onready var restart_btn: Button = $Panel/VBox/RestartButton
@onready var menu_btn: Button = $Panel/VBox/MenuButton
@onready var panel: Panel = $Panel

func _ready() -> void:
	resume_btn.pressed.connect(_on_resume)
	restart_btn.pressed.connect(_on_restart)
	menu_btn.pressed.connect(_on_menu)
	visible = false
	process_mode = Node.PROCESS_MODE_ALWAYS
	# Style
	_style_panel()
	_style_button(resume_btn, Color(0.2, 0.6, 1.0))
	_style_button(restart_btn, Color(0.45, 0.35, 0.2))
	_style_button(menu_btn, Color(0.35, 0.3, 0.45))

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
	style.border_color = Color(0.3, 0.5, 1.0, 0.4)
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

func _process(_delta: float) -> void:
	if GameManager.current_state == GameManager.GameState.PAUSED:
		if not visible:
			visible = true
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	else:
		visible = false

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		if GameManager.current_state == GameManager.GameState.PAUSED:
			_on_resume()

func _on_resume() -> void:
	GameManager.resume_game()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _on_restart() -> void:
	get_tree().paused = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	get_tree().reload_current_scene()

func _on_menu() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
