extends CanvasLayer
# HUD - Shows cleanliness, time, damage, current tool

@onready var cleanliness_bar: ProgressBar = $HUD/CleanlinessBar
@onready var cleanliness_label: Label = $HUD/CleanlinessLabel
@onready var time_label: Label = $HUD/TimeLabel
@onready var damage_label: Label = $HUD/DamageLabel
@onready var tool_label: Label = $HUD/ToolLabel
@onready var crosshair: Label = $HUD/Crosshair
@onready var message_label: Label = $HUD/MessageLabel
@onready var tip_label: Label = $HUD/TipLabel
@onready var cleanliness_panel: Panel = $HUD/CleanlinessPanel
@onready var time_panel: Panel = $HUD/TimePanel
@onready var tool_panel: Panel = $HUD/ToolPanel
@onready var interact_prompt: Label = $HUD/InteractPrompt if has_node("HUD/InteractPrompt") else null
@onready var buff_label: Label = $HUD/BuffLabel if has_node("HUD/BuffLabel") else null

var message_timer: float = 0.0
var FUNNY_TIPS = [
	"Tip: The mop goes back and forth. Try to make that happen.",
	"Tip: Vases are expensive. Worth more than your life.",
	"Tip: You CAN sprint. You probably shouldn't.",
	"Tip: Q switches tools. E interacts.",
	"Tip: Press Escape to give up temporarily.",
	"Tip: The bucket spills if you look at it wrong.",
	"Tip: Physics are working as intended.",
	"Tip: Breaking things costs money you don't have.",
	"Tip: Cleaning is optional. Keeping your job isn't.",
]
var tip_timer: float = 0.0
var tip_idx: int = 0

const TOOL_EMOJIS = {
	"mop": "🧹",
	"sponge": "🧽",
	"broom": "🪥",
	"spray": "💧",
}

func _ready() -> void:
	add_to_group("hud")
	GameManager.cleanliness_changed.connect(_on_cleanliness_changed)
	GameManager.damage_changed.connect(_on_damage_changed)
	GameManager.tool_changed.connect(_on_tool_changed)
	if damage_label:
		damage_label.text = "Damage: $0 / $2000"
		damage_label.modulate = Color(0.4, 1.0, 0.5)
	if tip_label:
		tip_label.text = FUNNY_TIPS[0]
	# Style panels with semi-transparent dark background
	_style_panel(cleanliness_panel)
	_style_panel(time_panel)
	_style_panel(tool_panel)

func _style_panel(panel: Panel) -> void:
	if not panel:
		return
	var style = StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.05, 0.1, 0.65)
	style.corner_radius_top_left = 8
	style.corner_radius_top_right = 8
	style.corner_radius_bottom_left = 8
	style.corner_radius_bottom_right = 8
	style.border_width_bottom = 2
	style.border_color = Color(0.3, 0.5, 1.0, 0.3)
	panel.add_theme_stylebox_override("panel", style)

func _process(delta: float) -> void:
	if message_timer > 0:
		message_timer -= delta
		if message_timer <= 0 and message_label:
			message_label.visible = false
	
	# Update mushroom buff display
	var player = get_tree().get_first_node_in_group("player")
	if player and buff_label:
		if player.active_buff_name != "" and player.buff_duration > 0:
			buff_label.text = "⚡ %s (%.1fs)" % [player.active_buff_name, player.buff_duration]
			buff_label.visible = true
		else:
			buff_label.visible = false

	# Update time
	if time_label and GameManager.current_state == GameManager.GameState.PLAYING:
		var remaining = GameManager.get_time_remaining()
		time_label.text = GameManager.format_time(remaining)
		if remaining < 60.0:
			time_label.modulate = Color(1.0, 0.3, 0.1)
		else:
			time_label.modulate = Color(1.0, 1.0, 1.0)
	# Rotate tips
	tip_timer += delta
	if tip_timer > 8.0:
		tip_timer = 0.0
		tip_idx = (tip_idx + 1) % FUNNY_TIPS.size()
		if tip_label:
			var t = get_tree().create_tween()
			t.tween_property(tip_label, "modulate:a", 0.0, 0.3)
			t.tween_callback(func(): tip_label.text = FUNNY_TIPS[tip_idx])
			t.tween_property(tip_label, "modulate:a", 0.7, 0.3)

func _on_cleanliness_changed(value: float) -> void:
	if cleanliness_bar:
		var t = get_tree().create_tween()
		t.tween_property(cleanliness_bar, "value", value, 0.5)
	if cleanliness_label:
		cleanliness_label.text = "Clean: %d%%" % int(value)
		if value > 80:
			cleanliness_label.modulate = Color(0.3, 1.0, 0.5)
		elif value > 50:
			cleanliness_label.modulate = Color(1.0, 1.0, 0.3)
		else:
			cleanliness_label.modulate = Color(1.0, 0.4, 0.3)

func _on_damage_changed(amount: float) -> void:
	if damage_label:
		damage_label.text = "Damage: $%.0f / $2000" % amount
		if amount >= 1500:
			damage_label.modulate = Color(1.0, 0.15, 0.15) # Red danger
			var t = get_tree().create_tween()
			t.tween_property(damage_label, "scale", Vector2(1.15, 1.15), 0.12)
			t.tween_property(damage_label, "scale", Vector2(1.0, 1.0), 0.12)
		elif amount >= 600:
			damage_label.modulate = Color(1.0, 0.6, 0.15) # Warning orange
		else:
			damage_label.modulate = Color(0.4, 1.0, 0.5) # Safe green
	if amount > 0:
		show_message("BROKE SOMETHING! -$%.0f (Limit: $2000)" % amount)

func _on_tool_changed(tool_name: String) -> void:
	if tool_label:
		var emoji = TOOL_EMOJIS.get(tool_name, "🧹")
		tool_label.text = "%s %s" % [emoji, tool_name.capitalize()]

func show_message(text: String) -> void:
	if message_label:
		message_label.text = text
		message_label.visible = true
		message_label.modulate.a = 1.0
		message_timer = 2.5
		# Pop-in effect
		message_label.scale = Vector2(1.3, 1.3)
		var t = get_tree().create_tween()
		t.tween_property(message_label, "scale", Vector2(1.0, 1.0), 0.2).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
