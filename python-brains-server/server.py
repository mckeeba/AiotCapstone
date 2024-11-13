from flask import Flask, request, jsonify
from aiot_gpt import AiotGpt  # Import your AiotGpt class to generate responses

app = Flask(__name__)

# Initialize the AiotGpt class
aiot_gpt = AiotGpt()

# Define an API route for handling NPC conversations
@app.route('/npc_conversation', methods=['POST'])
def npc_conversation():
    data = request.json  # Expecting JSON data from Godot

    npc_name = data.get('npc_name')
    user_input = data.get('user_input')  # The player's input

    response = aiot_gpt.run_character_api(npc_name, user_input)
    print("User input: " + user_input)
    return jsonify({npc_name: response})


# character greets the player to start the interaction
@app.route('/npc_greeting', methods=['POST'])
def npc_greeting():
    data = request.json  # Expecting JSON data from Godot

    npc_name = data.get('npc_name')

    response = aiot_gpt.run_character_greeting(npc_name)
    return jsonify({npc_name: response})

# Run the Flask app on port 4200
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4200)
    print(app.json)
