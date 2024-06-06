import unittest
from spotify_api.api_handler import access_token, extract_top_songs

class TestApiHandler(unittest.TestCase):
    def setUp(self):
        self.client_id = "<your_client_id>"
        self.client_secret = "<your_client_secret>"
        self.access_token = access_token(self.client_id, self.client_secret)
    
    def test_access_token(self):
        self.assertIsNotNone(self.access_token)
    
    def test_extract_top_songs(self):
        data = extract_top_songs(self.access_token)
        self.assertIsInstance(data, dict)
        self.assertIn('items', data)
