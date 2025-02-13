extends CanvasLayer
@export var npc_name: String  # Name of the NPC for the HTTP request
@export var api_url: String = "http://localhost:4200/"  # Your Flask server URL

var dialogue = []
var current_dialogue_id = 0
var consecutive_dialogues = 0
var d_active = false
var awaiting_response = false  # To track if we're waiting for a server response
var http_request: HTTPRequest

func _ready():
	# Ensure HTTPRequest node is added to the scene
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
	$NinePatchRect3.visible = false
	$LineEdit3.visible = false  
	set_process_input(true)


func start():
	if d_active:
		return  # Prevent starting dialogue again if already active
	$NinePatchRect3.visible = true
	$LineEdit3.visible = true  # Show the input box for the player
	$LineEdit3.grab_focus()  # Give focus to the input box for typing
	d_active = true
	consecutive_dialogues = 0  # Start with the first dialogue entry
	
	var player = get_parent().get_parent().get_node("Player")
	player.set_can_move(false)

	next_script()
	
func next_script():
	if awaiting_response:
		# If still waiting response, don't proceed to the next dialogue
		return
	
	# Move to the next dialogue entry
	if consecutive_dialogues == 0:
		# On the first interaction, trigger the HTTP request to the server
		send_greeting_request_to_server()
	else:
		# Continue to the next dialogue line
		if current_dialogue_id < dialogue.size():
			show_dialogue(current_dialogue_id)
			current_dialogue_id += 1
		else:
			# Allow the player to respond by typing into the input box
			$LineEdit3.visible = true
			$LineEdit3.grab_focus()

func show_dialogue(index: int):
	if index < dialogue.size():
		$NinePatchRect3/Name3.text = "Sarah"
		$NinePatchRect3/Chat3.text = dialogue[index]['text']

# Function to send HTTP request to the server
func send_convo_request_to_server(user_input: String):
	var json_data = {
		"npc_name": 'daughter',
		"user_input": user_input
	}
	var json_string = JSON.stringify(json_data)

	awaiting_response = true  # Mark that we are waiting for a response

	# Make an HTTP request to the server 
	http_request.request(
		api_url + 'npc_conversation',  # URL of the Flask server
		["Content-Type: application/json"],  # Request headers
		HTTPClient.METHOD_POST,  # HTTP method
		json_string  # Data to send in the body
	)
	
func send_greeting_request_to_server():
	var json_data = {
		"npc_name": 'daughter',
	}
	var json_string = JSON.stringify(json_data)

	awaiting_response = true  #  waiting for a response

	# Make an HTTP request to the server 
	http_request.request(
		api_url + 'npc_greeting',  
		["Content-Type: application/json"],  
		HTTPClient.METHOD_POST,
		json_string  
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
			
			#response is ready, show the next dialogue
			show_dialogue(current_dialogue_id)
			current_dialogue_id += 1
			consecutive_dialogues += 1
		else:
			print("Error parsing server response")
	else:
		print("HTTP request failed with response code: ", response_code)

# Function to end the dialogue session
func end_dialogue():
	$NinePatchRect3.visible = false  # Hide the UI
	$LineEdit3.visible = false  # Hide the input box
	d_active = false
	print("Dialogue finished")

func _input(event):
	# Check for mouse clicks or pressing Enter/Space to advance dialogue
	if d_active and (event is InputEventMouseButton and event.is_pressed() or event.is_action_pressed("ui_accept")):
		# If input box is visible, check for player input
		if $LineEdit3.visible and $LineEdit3.text != "" and event.keycode == KEY_ENTER:
			# Send player's input to the server
			send_convo_request_to_server($LineEdit3.text)
			$LineEdit3.text = ""  # Clear the input field after sending
			$LineEdit3.visible = false  # Hide input box after sending
		else:
			# Proceed to the next dialogue if no input is expected
			next_script()
	# End dialogue with the escape key
	if d_active and event.is_action_pressed("ui_cancel"):
		var player = get_parent().get_parent().get_node("Player")
		player.set_can_move(true)
		end_dialogue()
	
