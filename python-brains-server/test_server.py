import unittest
from unittest.mock import patch, MagicMock
from server import app  # Import your Flask app


class TestServer(unittest.TestCase):
    @patch("aiot_gpt.subprocess.run")
    @patch("server.aiot_gpt.run_character_api")
    def setUp(self, mock_run_character_api, mock_subprocess_run):
        """Set up the Flask test client and mock AiotGpt."""
        self.mock_subprocess_run = mock_subprocess_run
        self.mock_subprocess_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=0),
            MagicMock(stdout="mocked_api_key", returncode=0),
        ]
        self.mock_run_character_api = mock_run_character_api
        self.app = app.test_client()
        self.app.testing = True

    def test_npc_conversation(self):
        """Test the /npc_conversation endpoint."""
        self.mock_run_character_api.return_value = "Hello, traveler!"
        response = self.app.post(
            "/npc_conversation",
            json={"npc_name": "wizard", "user_input": "What is your wisdom?"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"wizard": "Hello, traveler!"})
        self.mock_run_character_api.assert_called_once_with("wizard", "What is your wisdom?")
