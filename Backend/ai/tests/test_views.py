from django.test import TestCase, Client
from django.urls import reverse
import json
import asyncio
from ..ai_response import Chatbot

class ChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('chat')
        self.chatbot = Chatbot()

    def test_simple_ai_response(self):
        """Simple test to print AI response"""
        print("\n=== Starting AI Response Test ===")
        
        # Direct AI response test
        test_message = "Say 'Hello, testing!' in a friendly way"
        response = asyncio.run(self.chatbot.get_response(test_message))
        print(f"\nDirect AI Response: {response}")
        
        # API endpoint test
        api_response = self.client.post(
            self.chat_url,
            data=json.dumps({'message': test_message}),
            content_type='application/json'
        )
        
        print(f"\nAPI Test Message: {test_message}")
        print(f"API Response Status: {api_response.status_code}")
        print(f"API Response Content: {api_response.json()}")
        print("\n=== Test Complete ===")

    def test_debug_chat_view(self):
        """Debug test for chat view"""
        test_message = "Debug test message"
        
        # Set a variable to watch
        self.debug_var = "Testing debug"
        
        # Make the API call
        api_response = self.client.post(
            self.chat_url,
            data=json.dumps({'message': test_message}),
            content_type='application/json'
        )
        
        # Add assertions for debugging
        self.assertEqual(api_response.status_code, 200)
        self.assertIn('response', api_response.json()) 