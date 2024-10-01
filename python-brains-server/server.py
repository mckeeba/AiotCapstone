from flask import Flask, request, jsonify
from aiot_gpt import AiotGpt  # Import your AiotGpt class to generate responses

app = Flask(__name__)

# Initialize the AiotGpt class
aiot_gpt = AiotGpt()

# Define an API route for handling NPC conversations
@app.route('/npc_conversation', methods=['POST'])
def npc_conversation():
    data = request.json  # Expecting JSON data from Godot

    npc_name = data.get('npc_name')  # The NPC's name, e.g., "Evanora"
    user_input = data.get('user_input')  # The player's input

    # Generate NPC response using the AiotGpt logic
    response = aiot_gpt.run_character(npc_name, user_input)

    # Return the response in JSON format
    return jsonify({'npc_response': response})

# Run the Flask app on port 4200
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4200)
