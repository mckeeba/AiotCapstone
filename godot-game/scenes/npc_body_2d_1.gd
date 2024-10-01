extends CharacterBody2D

@onready var interaction_area = $Area2D  # Reference to the Area2D child node

func _ready():
	# Use Callable to connect signals from Area2D
	interaction_area.connect("body_entered", Callable(self, "_on_body_entered"))
	interaction_area.connect("body_exited", Callable(self, "_on_body_exited"))

func _on_body_entered(body):
	# Enable interaction when the Player enters the NPC's interaction area
	if body.name == "Player":
		# Trigger the dialogue start() function in dialoguePlayer.gd
		var dialogue = get_parent().get_node("MedicineWoman/Dialogue")  # Adjust the path to your Dialogue node
		if dialogue:
			dialogue.start()

func _on_body_exited(body):
	# Optional: Handle what happens when the player leaves the interaction area
	if body.name == "Player":
		print("Player exited the interaction area")
