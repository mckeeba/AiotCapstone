extends CanvasLayer

@export var dialogfile: String
var dialogue = []
var current_dialogue_id = 0
var d_active = false

func _ready():
	$NinePatchRect.visible = false
	set_process_input(true)
	

func start():
	if d_active:
		return  # Prevent starting dialogue again if already active
	$NinePatchRect.visible = true
	d_active = true
		
	dialogue = load_dialogue()
	current_dialogue_id = -1  # Start with the first dialogue entry
	next_script()

func next_script():
	# Move to the next dialogue entry
	current_dialogue_id += 1
	
	# Check if we've reached the end of the dialogue
	if current_dialogue_id < dialogue.size():
		show_dialogue(current_dialogue_id)
	else:
		$NinePatchRect.visible = false
		d_active = false

func show_dialogue(index: int):
	if index < dialogue.size():
		$NinePatchRect/Name.text = dialogue[index]['name']
		$NinePatchRect/Chat.text = dialogue[index]['text']

func load_dialogue():
	# Open the file with FileAccess
	var dialogue_file = FileAccess.open(dialogfile, FileAccess.READ)
	if dialogue_file:
		var content = dialogue_file.get_as_text()
		dialogue_file.close()

		# Instantiate JSON and parse the content
		var json = JSON.new()
		var parse_result = json.parse(content)

		# Check if parsing was successful (OK is a constant that equals 0)
		if parse_result == OK:
			return json.get_data()  # Use get_data() to retrieve the actual JSON data
		else:
			print("Error parsing JSON")
	else:
		print("Error opening file: ", dialogfile)
	return []

func _input(event):
	# Check for mouse clicks or pressing Enter/Space to advance dialogue
	if d_active and (event is InputEventMouseButton and event.is_pressed() or event.is_action_pressed("ui_accept")):
		next_script()
