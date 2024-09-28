extends Area2D


func input(event):
	if event is InputEventMouseButton and event.is_pressed() or event.is_action_pressed("ui_accept") and len(get_overlapping_bodies()) > 0:
		use_dialogue()

func use_dialogue():
	var dialogue = get_parent().get_node("Dialogue")
	if dialogue:
		dialogue.start()
		
