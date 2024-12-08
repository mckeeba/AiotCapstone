import unittest
from unittest.mock import MagicMock, patch
import os
import json
from aiot_gpt import AiotGpt
class TestAiotGpt(unittest.TestCase):

    @patch("subprocess.run")
    def setUp(self, mock_subprocess_run):
        """Set up a test instance of the AiotGpt class and mock OpenAI client."""
        mock_subprocess_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=0),
            MagicMock(stdout="mocked_api_key", returncode=0),
        ]
        self.aiot_gpt = AiotGpt()
        self.aiot_gpt.client = MagicMock()
        self.test_files = {
            'wizard': 'wizard.json',
            'medicine_woman': 'medicine_woman.json',
            'blacksmith': 'blacksmith.json',
            'daughter': 'daughter.json',
            'goblin': 'goblin.json'
        }
        for file in self.test_files.values():
            with open(file, 'w') as f:
                json.dump([], f)

    def tearDown(self):
        """Remove test JSON files after each test."""
        for file in self.test_files.values():
            if os.path.exists(file):
                os.remove(file)

    def test_reset_json_files(self):
        """Test if JSON files are reset properly."""
        for file in self.test_files.values():
            with open(file, 'w') as f:
                json.dump([{"test": "data"}], f)

        self.aiot_gpt.reset_json_files()

        # Verify all files are empty
        for file in self.test_files.values():
            with open(file, 'r') as f:
                data = json.load(f)
                self.assertEqual(data, [])

    def test_append_to_json(self):
        """Test appending data to a JSON file."""
        test_file = self.test_files['wizard']
        self.aiot_gpt.append_to_json(test_file, {"name": "Alabaster", "text": "Hello, traveler!"})

        with open(test_file, 'r') as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Alabaster")
        self.assertEqual(data[0]["text"], "Hello, traveler!")

    def test_load_json(self):
        """Test loading data from a JSON file."""
        test_file = self.test_files['wizard']
        with open(test_file, 'w') as f:
            json.dump([{"name": "Alabaster"}], f)

        data = self.aiot_gpt.load_json(test_file)
        self.assertEqual(data, [{"name": "Alabaster"}])

    def test_load_json_file_not_found(self):
        """Test loading data from a non-existent JSON file."""
        data = self.aiot_gpt.load_json('non_existent.json')
        self.assertEqual(data, [])

    def test_run_character_greeting(self):
        """Test the run_character_greeting method."""
        self.aiot_gpt.client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                model_dump_json=MagicMock(
                    return_value=json.dumps({"message": {"content": "Greetings, adventurer!"}})
                )
            )]
        )

        response = self.aiot_gpt.run_character_greeting('wizard')

        self.assertIn("Greetings, adventurer!", response)
        self.aiot_gpt.client.chat.completions.create.assert_called_once()

    def test_run_character_api(self):
        """Test the run_character_api method."""
        self.aiot_gpt.client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(content="Here is your response.")
            )]
        )

        response = self.aiot_gpt.run_character_api('wizard', 'What is your wisdom?')

        self.assertEqual(response, "Here is your response.")
        self.aiot_gpt.client.chat.completions.create.assert_called_once()

    def test_invalid_character_greeting(self):
        """Test handling invalid character input in run_character_greeting."""
        with self.assertRaises(ValueError):
            self.aiot_gpt.run_character_greeting('invalid_character')

    def test_invalid_character_api(self):
        """Test handling invalid character input in run_character_api."""
        with self.assertRaises(ValueError):
            self.aiot_gpt.run_character_api('invalid_character', 'Any input')

if __name__ == '__main__':
    unittest.main()
