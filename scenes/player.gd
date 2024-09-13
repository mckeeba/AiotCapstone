extends CharacterBody2D

@onready var animated_sprite_2d = $AnimatedSprite2D
@export var speed = 400

func get_input():
	# Get the direction vector based on input actions
	var input_direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_direction * speed

	# Check which key is pressed and play the animation
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
		# Stop animation if no movement key is pressed
		animated_sprite_2d.stop()

func _physics_process(_delta):
	get_input()
	move_and_slide()
