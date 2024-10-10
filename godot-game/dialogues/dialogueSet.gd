extends CanvasLayer
@export var npc_name: String  # Name of the NPC for the HTTP request
@export var api_url: String = "http://localhost:4200/npc_conversation"  # Your Flask server URL

var dialogue = []
var current_dialogue_id = 0
var d_active = false
var http_request: HTTPRequest

func _ready():
	# Ensure HTTPRequest node is added to the scene
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
	
	$NinePatchRect.visible = false
	set_process_input(true)


func start():
	if d_active:
		return  # Prevent starting dialogue again if already active
	$NinePatchRect.visible = true
	d_active = true
	
	current_dialogue_id = -1  # Start with the first dialogue entry
	next_script()

func next_script():
	# Move to the next dialogue entry
	current_dialogue_id += 1

	if current_dialogue_id == 0:
		# On the first interaction, trigger the HTTP request to the server
		send_request_to_server("hello, i'm new in town")
	else:
		# Continue to the next dialogue line
		if current_dialogue_id < dialogue.size():
			show_dialogue(current_dialogue_id)
		else:
			$NinePatchRect.visible = false
			d_active = false

func show_dialogue(index: int):
	if index < dialogue.size():
		$NinePatchRect/Name.text = dialogue[index]['name']
		$NinePatchRect/Chat.text = dialogue[index]['text']

# Function to send HTTP request to the server
func send_request_to_server(user_input: String):
	var json_data = {
		"npc_name": "wizard",
		"user_input": user_input
	}
	var json_string = JSON.stringify(json_data)

	# Make an HTTP request to the server (non-blocking)
	http_request.request(
		api_url,  # URL of the Flask server
		["Content-Type: application/json"],  # Request headers
		HTTPClient.METHOD_POST,  # HTTP method
		json_string  # Data to send in the body
		)


# Callback function for when the request is completed
func _http_request_completed(result, response_code, headers, body):
	if response_code == 200:
		# Successfully got a response from the server
		var json = JSON.new()
		var parse_result = json.parse(body.get_string_from_utf8())
		
		if parse_result == OK:
			var response_data = json.get_data()
			# Store the dialogue response in the dialogue array
			for npc in response_data.keys():
				dialogue.append({"name": npc, "text": response_data[npc]})
			next_script()  # Show the received dialogue
		else:
			print("Error parsing server response")
	else:
		print("HTTP request failed with response code: ", response_code)

func _input(event):
	# Check for mouse clicks or pressing Enter/Space to advance dialogue
	if d_active and (event is InputEventMouseButton and event.is_pressed() or event.is_action_pressed("ui_accept")):
		next_script()
