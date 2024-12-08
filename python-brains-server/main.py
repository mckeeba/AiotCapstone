import openai
import json
import aiot_gpt
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
            AIOT.run_character_greeting('wizard')
        elif choice == 'm':
            AIOT.run_character_greeting('medicine woman')
        elif choice == 'b':
            AIOT.run_character_greeting('blacksmith')
        elif choice == 'bd':
            (AIOT.run_character_greeting('daughter'))
        elif choice == 'g':
            AIOT.run_character_greeting('goblin')
        elif choice == 'quit':
            break
        else:
            print("invalid choice.")
