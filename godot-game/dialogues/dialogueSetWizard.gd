extends CanvasLayer
@export var npc_name: String  # Name of the NPC for the HTTP request
@export var api_url: String = "http://localhost:4200/npc_conversation"  # Your Flask server URL

var dialogue = []
var current_dialogue_id = 0
var d_active = false
var awaiting_response = false  # To track if we're waiting for a server response
var http_request: HTTPRequest

func _ready():
	# Ensure HTTPRequest node is added to the scene
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
	$NinePatchRect5.visible = false
	$LineEdit5.visible = false  # Hide input box until needed
	set_process_input(true)


func start():
	if d_active:
		return  # Prevent starting dialogue again if already active
	$NinePatchRect5.visible = true
	$LineEdit5.visible = true  # Show the input box for the player
	$LineEdit5.grab_focus()  # Give focus to the input box for typing
	d_active = true
	current_dialogue_id = 0  # Start with the first dialogue entry
	next_script()
	
func next_script():
	if awaiting_response:
		# If we're still waiting for the response, don't proceed to the next dialogue
		return
	
	# Move to the next dialogue entry
	if current_dialogue_id == 0:
		# On the first interaction, trigger the HTTP request to the server
		send_request_to_server("hello, I'm new in town")
	else:
		# Continue to the next dialogue line
		if current_dialogue_id < dialogue.size():
			show_dialogue(current_dialogue_id)
			current_dialogue_id += 1
		else:
			# Allow the player to respond by typing into the input box
			$LineEdit5.visible = true
			$LineEdit5.grab_focus()

func show_dialogue(index: int):
	if index < dialogue.size():
		$NinePatchRect5/Name5.text = dialogue[index]['name']
		$NinePatchRect5/Chat5.text = dialogue[index]['text']

# Function to send HTTP request to the server
func send_request_to_server(user_input: String):
	var json_data = {
		"npc_name": 'wizard',
		"user_input": user_input
	}
	var json_string = JSON.stringify(json_data)

	awaiting_response = true  # Mark that we are waiting for a response

	# Make an HTTP request to the server (non-blocking)
	http_request.request(
		api_url,  # URL of the Flask server
		["Content-Type: application/json"],  # Request headers
		HTTPClient.METHOD_POST,  # HTTP method
		json_string  # Data to send in the body
	)

# Callback function for when the request is completed
func _http_request_completed(result, response_code, headers, body):
	awaiting_response = false  # Reset the waiting flag

	if response_code == 200:
		# Successfully got a response from the server
		var json = JSON.new()
		var parse_result = json.parse(body.get_string_from_utf8())
		
		if parse_result == OK:
			var response_data = json.get_data()
			# Store the dialogue response in the dialogue array
			for npc in response_data.keys():
				dialogue.append({"name": npc, "text": response_data[npc]})
			
			# Now that the response is ready, show the next dialogue
			show_dialogue(current_dialogue_id)
			current_dialogue_id += 1
		else:
			print("Error parsing server response")
	else:
		print("HTTP request failed with response code: ", response_code)

# Function to end the dialogue session
func end_dialogue():
	$NinePatchRect5.visible = false
	$LineEdit5.visible = false
	d_active = false
	print("Dialogue finished")

func _input(event):
	# Check for mouse clicks or pressing Enter/Space to advance dialogue
	if d_active and (event is InputEventMouseButton and event.is_pressed() or event.is_action_pressed("ui_accept")):
		# If input box is visible, check for player input
		if $LineEdit5.visible and $LineEdit5.text != "" and event.keycode == KEY_ENTER:
			# Send player's input to the server
			send_request_to_server($LineEdit5.text)
			$LineEdit5.text = ""  # Clear the input field after sending
			$LineEdit5.visible = false  # Hide input box after sending
		else:
			# Proceed to the next dialogue if no input is expected
			next_script()
	# End dialogue with the escape key
	if d_active and event.is_action_pressed("ui_cancel"):
		end_dialogue()