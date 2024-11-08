extends Area2D

func _ready():
	connect("body_entered", Callable(self, "_on_body_entered"))
	connect("body_exited", Callable(self, "_on_body_exited"))

func _on_body_entered(body):
	# Check if the player has entered the NPC's interaction area
	if body.name == "Player":
		body.can_interact = true  # Enable interaction from player.gd

func _on_body_exited(body):
	# Check if the player has left the NPC's interaction area
	if body.name == "Player":
		body.can_interact = false  # Disable interaction from player.gd

func trigger_dialogue():
	var dialogue = get_parent().get_node("DialogueWiz")
	if dialogue:
		dialogue.start()  # Start the dialogue when triggered
