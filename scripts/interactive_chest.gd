extends StaticBody3D
# Interactive wooden chest with loot/bonus cash

@export var is_open: bool = false
@onready var lid: MeshInstance3D = $Lid if has_node("Lid") else null

func _ready() -> void:
	add_to_group("interactable")

func get_interaction_text() -> String:
	return "" if is_open else "[E] Open Chest"

func interact(player: Node) -> void:
	if is_open:
		return
	is_open = true
	ProceduralAudio.play_score_tick(self)
	
	if lid:
		var t = get_tree().create_tween()
		t.tween_property(lid, "rotation_degrees:x", -75.0, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	else:
		var t = get_tree().create_tween()
		t.tween_property(self, "scale", Vector3(1.08, 1.15, 1.08), 0.12).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		t.tween_property(self, "scale", Vector3(1.0, 1.0, 1.0), 0.20)

	if GameManager.has_method("add_score"):
		GameManager.add_score(150.0)
	elif "score" in GameManager:
		GameManager.score += 150.0
	_show_popup("CHEST OPENED! +$150")

func _show_popup(text: String) -> void:
	var l = Label3D.new()
	l.text = text
	l.modulate = Color(1.0, 0.85, 0.2)
	l.font_size = 64
	l.outline_size = 12
	l.outline_modulate = Color(0, 0, 0, 0.95)
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	add_child(l)
	l.position = Vector3(0, 0.8, 0)
	var t = get_tree().create_tween()
	t.tween_property(l, "position", Vector3(0, 1.8, 0), 1.4)
	t.parallel().tween_property(l, "modulate:a", 0.0, 1.4)
	t.tween_callback(l.queue_free)
