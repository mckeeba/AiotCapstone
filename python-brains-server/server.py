
from flask import Flask, request, jsonify
from aiot_gpt import AiotGpt

app = Flask(__name__)

aiot_gpt = AiotGpt()

@app.route('/npc_conversation', methods=['POST'])
def npc_conversation():
    data = request.json
    npc_name = data.get('npc_name')
    user_input = data.get('user_input')
    response = aiot_gpt.run_character_api(npc_name, user_input)
    print("User input: " + user_input)
    return jsonify({npc_name: response})


@app.route('/npc_greeting', methods=['POST'])
def npc_greeting():
    data = request.json
    npc_name = data.get('npc_name')
    response = aiot_gpt.run_character_greeting(npc_name)
    return jsonify({npc_name: response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4200, use_reloader=False)
    print(app.json)
