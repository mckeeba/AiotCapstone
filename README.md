# AiotCapstone
AiotCapstone is a 2D top-down game where the NPCs are powered by ChatGPT. Each NPC has their own unique personality, memory, and role within the game world. Additionally, NPCs are aware of each other's existence and actions, creating a dynamic and interactive game environment.

## NPCs
The game features the following NPCs, each with their own distinct traits and backstory:

1. **Alabaster, the Wizard**  
   The sage and leader of the village. Alabaster's wisdom and foresight guide the village, but his whimsical and eclectic nature, especially when discussing his magic, makes him a fascinating character.

2. **Evanora, the Medicine Woman**  
   The caretaker of the village, tending to wounds and offering whimsical herbal remedies along with encouraging words of wisdom.

3. **Haus, the Blacksmith**  
   A tough, determined, and cranky blacksmith with a soft spot for his adopted daughter, Sarah.

4. **Sarah, Daughter of the Blacksmith**  
   Sweet and innocent, Sarah loves bugs, plants, and animals. She deeply admires and loves her father, Haus.

5. **Glork, the Goblin**  
   Cartoonishly evil, Glork is always scheming to wreak havoc on the village. He lives in a cave up in the mountains.

Feel free to explore the NPCs' unique perspectives, personalities, and interactions within the game!

---

## How to Run the Game

## Prerequisites
Before setting up the game, ensure you have the following installed on your system:

- **Python** (latest version recommended)
- **Godot Game Engine** (free download: [https://godotengine.org/](https://godotengine.org/))

## Setup Steps

### 1. Install Python
Ensure Python is installed on your system. If not, follow these steps:

- **Windows:**
  1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
  2. Run the installer and **check** the option to **"Add Python to PATH"** before installing.
  3. Open a terminal (Command Prompt or PowerShell) and verify installation by running:
     ```sh
     python --version
     ```
  
- **Mac/Linux:**
  1. Open a terminal and check if Python is installed:
     ```sh
     python3 --version
     ```
  2. If not installed, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/) or install via:
     - **Mac:**  
       ```sh
       brew install python
       ```
     - **Linux:**  
       ```sh
       sudo apt install python3
       ```

### 2. Download and Set Up Godot
1. Download and install Godot from [https://godotengine.org/](https://godotengine.org/).
2. Open **Godot** and click **"Import"**.
3. Navigate to the project directory:
   ```sh
   /<your download location>/AiotCapstone/godot-game/

## 3. Running the Game

### 1. Start the Flask Server
The Flask server powers the AI-driven NPCs. You need to start it before launching the game.

- **Using the Command Line:**
  1. Open a terminal and navigate to the root directory of `AiotCapstone`.
  2. Run the appropriate command for your operating system:
     - **Windows:**
       ```sh
       python python-brains-server/server.py
       ```
     - **Mac/Linux:**
       ```sh
       python python-brains-server/server.py
       ```

- **Using an IDE (e.g., VS Code, PyCharm):**
  1. Open `server.py` from the `python-brains-server` directory.
  2. Click **Run** or use the IDE’s built-in terminal to execute:
     ```sh
     python server.py
     ```
  The command terminal will then take you through a few steps you will follow to log in and register.

### 2. Launch the Game in Godot
1. Open **Godot**.
2. Select the `AIOT` project.
3. Click **Run** to start the game.

---

## Explore the Game
Immerse yourself in a world where NPCs are more than just background characters. Each character has their own story, unique interactions, and the ability to adapt dynamically to your actions. Enjoy the experience!

---


    

