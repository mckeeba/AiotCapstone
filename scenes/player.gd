extends CharacterBody2D

@onready var animated_sprite_2d = $AnimatedSprite2D
@export var speed = 400

var can_interact = false  # Track if the player can interact with an NPC

func get_input():
	var input_direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_direction * speed

	# Handle animations
	if Input.is_action_pressed("move_up"):
		if animated_sprite_2d.animation != "move_up" or !animated_sprite_2d.is_playing():
			animated_sprite_2d.play("move_up")
	elif Input.is_action_pressed("move_down"):
		if animated_sprite_2d.animation != "move_down" or !animated_sprite_2d.is_playing():
			animated_sprite_2d.play("move_down")
	elif Input.is_action_pressed("move_left"):
		if animated_sprite_2d.animation != "move_left" or !animated_sprite_2d.is_playing():
			animated_sprite_2d.play("move_left")
			animated_sprite_2d.flip_h = false
	elif Input.is_action_pressed("move_right"):
		if animated_sprite_2d.animation != "move_right" or !animated_sprite_2d.is_playing():
			animated_sprite_2d.play("move_right")
			animated_sprite_2d.flip_h = true
	else:
		animated_sprite_2d.stop()

func _physics_process(_delta):
	get_input()
	move_and_slide()

func _process(delta):
	# Check for interaction when the player presses the interact key
	if can_interact and Input.is_action_just_pressed("ui_accept"):
		# Find the NPC by its path and trigger dialogue
		var npc = get_node_or_null("/root/Environment2D/MedicineWoman")
		if npc:
			npc.trigger_dialogue()
