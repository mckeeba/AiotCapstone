import openai
import json
import user_auth

SECRET = "python-brains-server/aiot_gpt/chat_gpt-api-key"
USER_POOL_ID = "us-east-1_YREP5IfxE"
CLIENT_ID = "69f24j17t7k18eoji251dauinu"
IDENTITY_POOL_ID = "us-east-1:5b8f1a30-c810-4665-849a-bc7845e090f8"
REGION = "us-east-1"

class AiotGpt:
    def __init__(self):
        if not openai.api_key:
            self.get_key()

        # Initialize the OpenAI client
        self.client = openai.OpenAI(
            api_key=openai.api_key,
        )

        self.interact_counts = {
            'wizard': 0,
            'medicine woman': 0,
            'blacksmith': 0,
            'daughter': 0,
            'goblin': 0
        }

        self.file_paths = {
            'wizard': 'wizard.json',
            'medicine_woman': 'medicine_woman.json',
            'blacksmith': 'blacksmith.json',
            'daughter': 'daughter.json',
            'goblin': 'goblin.json'
        }

        self.reset_json_files()

        # Base system messages shared across all NPCs
        base_context = [{
            "role": "system",
            "content": "Your job is to simulate NPCs in a small top-down RPG game taking place in a village on an island called Telmaron. \n"
                       "Of the NPCs that you will simulate, there are 5 characters: \n"
                       "1. Alabaster, the wizard - The sage and leader of the village, Alabaster's wisdom and foresight is the guiding will of the village. He is also very whimsical and eclectic, especially when he talks about his magic.\n"
                       "2. Evanora, the medicine woman - She takes care of the village and tends to the wounds of your kin. She offers whimsical herbal remedies and encouraging words of wisdom.\n"
                       "3. Haus, the blacksmith - A tough, determined, cranky blacksmith with a sweet spot for his daughter.\n"
                       "4. Sarah, daughter of the blacksmith - The adopted daughter of the blacksmith. She is innocent and sweet and loves bugs, plants, and animals. She loves and admires her father.\n"
                       "5. Glork, the Goblin - Cartoonishly evil, Glork is always devising some evil scheme to wreak havoc on the village. He lives in a cave up the mountain.\n"
        }, {
            "role": "system",
            "content": "do not talk in third person"
        }, {
            "role": "system",
            "content": "NPCs will not interact directly. They will stay around their respective posts"
        }]

        self.wizard_logs = base_context.copy() + [{
            "role": "system",
            "content": 'You are Alabaster, a wizard in an RPG game. You will be interacting with players as you give them whimsical words of wisdom. Your name is Alabaster.'
        }]

        self.medicine_woman_logs = base_context.copy() + [{
            "role": "system",
            "content": 'You are Evanora, a medicine woman in an RPG game. You take care of the village and tend to the wounds of your kin. You offer whimsical herbal remedies and encouraging words of wisdom.'
        }]

        self.blacksmith_logs = base_context.copy() + [{
            "role": "system",
            "content": 'You are Haus, a blacksmith in an RPG game. You are tough, determined, cranky, but have a sweet spot for your daughter (she is a child). You offer armor and weapon upgrades and sarcastic dialogue.'
        }]

        self.daughter_logs = base_context.copy() + [{
            "role": "system",
            "content": 'You are Sarah, the young daughter of the blacksmith in an RPG game. You are innocent and sweet and love bugs and your toys. You love and admire your father, who is a blacksmith.'
        }]

        self.goblin_logs = base_context.copy() + [{
            "role": "system",
            "content": 'You are Glork, a goblin in an RPG game. You are dastardly and conniving as you are whimsical. You are always scheming to cause mischief over the people down the mountain.'
        }]

    query = ''

    def get_key(self):
        id_token = self.authenticate_user()
        if id_token:
            aws_credentials = user_auth.get_aws_credentials(id_token)
            if aws_credentials:
                secret = user_auth.retrieve_secret(aws_credentials, SECRET)
                secret_dict = json.loads(secret)
                openai.api_key = secret_dict['AIOT_GPT']
        return 0

    def authenticate_user(self):
        id_token = False
        choice = input("Login or Register?(L/R):")
        if choice == "R":
            user_auth.register_user()
        elif choice == "L":
            id_token = user_auth.authenticate_user()
        else:
            print("Invalid input!")
            pass
        return id_token

    def reset_json_files(self):
        """Reset all character JSON files by overwriting them with empty data."""
        empty_data = []

        for character, file_path in self.file_paths.items():
            with open(file_path, 'w') as file:
                json.dump(empty_data, file, indent=4)

    def append_to_json(self, file_path, new_data):
        """Append new data to the existing JSON file."""
        data = self.load_json(file_path)  # Load the current JSON data

        if isinstance(data, list):
            data.append(new_data)
        else:
            data = [new_data]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_json(self, file_path):
        """Load existing data from a JSON file, or return an empty list if it doesn't exist."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def run_character_greeting(self, character):
        if character == 'wizard':
            chat_log = self.wizard_logs
            character_name = 'Alabaster, the wizard'
            file_path = 'wizard.json'
        elif character == 'medicine woman':
            chat_log = self.medicine_woman_logs
            character_name = 'Evanora, the medicine woman'
            file_path = 'medicine_woman.json'
        elif character == 'blacksmith':
            chat_log = self.blacksmith_logs
            character_name = 'Haus, the blacksmith'
            file_path = 'blacksmith.json'
        elif character == 'daughter':
            chat_log = self.daughter_logs
            character_name = 'Sarah, daughter of the blacksmith'
            file_path = 'daughter.json'
        elif character == 'goblin':
            chat_log = self.goblin_logs
            character_name = 'Glork, the Goblin'
            file_path = 'goblin.json'
        else:
            raise ValueError(f"Invalid character: {character}. Expected one of: "
                             "'wizard', 'medicine woman', 'blacksmith', 'daughter', 'goblin'.")

        print(self.interact_counts)
        if self.interact_counts[character] == 0:
            chat_log.append({
                "role": "system",
                "content": "A new stranger has arrived at your post."
            })
        else:
            chat_log.append({
                "role": "system",
                "content": "The player has returned to your post."
            })

        self.interact_counts[character] += 1
        print(self.interact_counts)

        query = ''
        while query != '_q':
            character_response = self.client.chat.completions.create(
                messages=chat_log,
                model="gpt-4o",
            )
            content = character_response.choices[0].model_dump_json()
            response = json.loads(content)['message']['content']

            chat_log.append({
                "role": "assistant",
                "content": response
            })

            self.append_to_json(file_path, {"name": character_name, "text": response})

            return response

    def run_character_api(self, character, user_input):
        # Select the appropriate chat log and character file based on the character name
        if character == 'wizard':
            chat_log = self.wizard_logs
            character_name = 'Alabaster, the wizard'
            file_path = 'wizard.json'
        elif character == 'medicine woman':
            chat_log = self.medicine_woman_logs
            character_name = 'Evanora, the medicine woman'
            file_path = 'medicine_woman.json'
        elif character == 'blacksmith':
            chat_log = self.blacksmith_logs
            character_name = 'Haus, the blacksmith'
            file_path = 'blacksmith.json'
        elif character == 'daughter':
            chat_log = self.daughter_logs
            character_name = 'Sarah, daughter of the blacksmith'
            file_path = 'daughter.json'
        elif character == 'goblin':
            chat_log = self.goblin_logs
            character_name = 'Glork, the Goblin'
            file_path = 'goblin.json'
        else:
            raise ValueError(
                f"Invalid character: {character}. Expected one of: 'wizard', 'medicine woman', 'blacksmith', 'daughter', 'goblin'.")

        # Append the user's query to the chat log
        chat_log.append({
            "role": "user",
            "content": user_input
        })

        # Get the response from the GPT model
        character_response = self.client.chat.completions.create(
            messages=chat_log,
            model="gpt-4o",
        )

        response = character_response.choices[0].message.content
        # Append the assistant's response to the chat log
        chat_log.append({
            "role": "assistant",
            "content": response
        })

        # Save the conversation to the appropriate character's file
        self.append_to_json(file_path, {"name": character_name, "text": response})

        # Return the response to the server
        return response

