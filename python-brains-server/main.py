import openai
import json
import aiot_gpt
openai.api_key = open("key.txt", 'r').read().strip('\n')  # host the api on an endpoint such that only the game can make calls to it
from openai import OpenAI

client = OpenAI(
    api_key=openai.api_key,
)

query = ''


if __name__ == "__main__":
    AIOT = aiot_gpt.AiotGpt()
    choice = ''
    while choice != 'quit':
        character_name = ''
        print("Choonse your character:")
        print("Wizard: [w]")
        print("Medicine woman: [m]")
        print("Blacksmith: [b]")
        print("Blacksmith's Daughter: [bd]")
        print("Goblin: [g]")
        choice = input("You: ")
        if choice == 'w':
            AIOT.run_character('wizard')
        elif choice == 'm':
            AIOT.run_character('medicine woman')
        elif choice == 'b':
            AIOT.run_character('blacksmith')
        elif choice == 'bd':
            AIOT.run_character('daughter')
        elif choice == 'g':
            AIOT.run_character('goblin')
        elif choice == 'quit':
            break
        else:
            print("invalid choice.")
