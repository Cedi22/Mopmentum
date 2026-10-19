extends Control

@onready var play_btn: Button = $VBox/PlayButton
@onready var quit_btn: Button = $VBox/QuitButton
@onready var title_label: Label = $TitleLabel
@onready var subtitle_label: Label = $SubtitleLabel
@onready var mop_emoji: Label = $MopEmoji

var float_time: float = 0.0

func _ready() -> void:
	play_btn.pressed.connect(_on_play)
	quit_btn.pressed.connect(_on_quit)
	# Style buttons with rounded look
	_style_button(play_btn, Color(0.2, 0.6, 1.0), Color(0.3, 0.7, 1.0))
	_style_button(quit_btn, Color(0.35, 0.3, 0.45), Color(0.45, 0.4, 0.55))
	# Animate title entrance
	if title_label:
		var t = get_tree().create_tween()
		title_label.modulate.a = 0.0
		title_label.position.y += 30
		t.tween_property(title_label, "modulate:a", 1.0, 1.2).set_ease(Tween.EASE_OUT)
		t.parallel().tween_property(title_label, "position:y", title_label.position.y - 30, 1.2).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	if subtitle_label:
		subtitle_label.modulate.a = 0.0
		var t2 = get_tree().create_tween()
		t2.tween_interval(0.6)
		t2.tween_property(subtitle_label, "modulate:a", 1.0, 0.8)
	# Animate buttons
	play_btn.modulate.a = 0.0
	quit_btn.modulate.a = 0.0
	var t3 = get_tree().create_tween()
	t3.tween_interval(1.0)
	t3.tween_property(play_btn, "modulate:a", 1.0, 0.5)
	t3.tween_property(quit_btn, "modulate:a", 1.0, 0.4)

func _process(delta: float) -> void:
	float_time += delta
	# Floating mop emoji
	if mop_emoji:
		mop_emoji.position.y = 400 + sin(float_time * 1.5) * 15.0
		mop_emoji.rotation = sin(float_time * 0.8) * 0.15

func _style_button(btn: Button, normal_color: Color, hover_color: Color) -> void:
	var style_normal = StyleBoxFlat.new()
	style_normal.bg_color = normal_color
	style_normal.corner_radius_top_left = 12
	style_normal.corner_radius_top_right = 12
	style_normal.corner_radius_bottom_left = 12
	style_normal.corner_radius_bottom_right = 12
	style_normal.content_margin_left = 20
	style_normal.content_margin_right = 20
	style_normal.content_margin_top = 10
	style_normal.content_margin_bottom = 10
	btn.add_theme_stylebox_override("normal", style_normal)
	var style_hover = style_normal.duplicate()
	style_hover.bg_color = hover_color
	btn.add_theme_stylebox_override("hover", style_hover)
	var style_pressed = style_normal.duplicate()
	style_pressed.bg_color = normal_color.darkened(0.2)
	btn.add_theme_stylebox_override("pressed", style_pressed)
	var style_focus = StyleBoxEmpty.new()
	btn.add_theme_stylebox_override("focus", style_focus)

func _on_play() -> void:
	var t = get_tree().create_tween()
	t.tween_property(self, "modulate:a", 0.0, 0.5)
	t.tween_callback(func(): get_tree().change_scene_to_file("res://levels/level_01.tscn"))

func _on_quit() -> void:
	get_tree().quit()
