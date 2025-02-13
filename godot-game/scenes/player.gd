extends CharacterBody2D

@onready var animated_sprite_2d = $AnimatedSprite2D
@export var speed = 400
var server_path = "../python-brains-server/server.py"
var can_interact = false  # Track if the player can interact with an NPC
var can_move = true

#func _ready():
	#start_python_server()
	#
#func start_python_server():
	#var pystdout = []
	#var python_executable = "python3"
	#
	#var result = OS.execute(python_executable, [server_path], pystdout, true)
	#
	#print(pystdout)
	#
	#if result == OK:
		#print("Python server started successfully.")
		#for line in pystdout:
				#print(line)
	#else:
		#print("Failed to start Python server. Error code:", result)
		
func get_input():
	if not can_move:
		velocity = Vector2.ZERO
		animated_sprite_2d.stop()
		return


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

func set_can_move(state: bool):
	can_move = state
