import unittest
import asyncio
from unittest.mock import patch, MagicMock
from Backend.ai.ai_response import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.chatbot = Chatbot()
        self.maxDiff = None
        self.buffer = False

    def test_init(self):
        """Test if chatbot initializes with correct system message"""
        self.assertEqual(len(self.chatbot.messages), 1)
        self.assertEqual(
            self.chatbot.messages[0],
            {"role": "system", "content": "You are a helpful assistant."}
        )

    def test_clear_history(self):
        """Test if chat history clears correctly"""
        # Add a message
        self.chatbot.messages.append({"role": "user", "content": "test message"})
        # Clear history
        self.chatbot.clear_history()
        # Check if only system message remains
        self.assertEqual(len(self.chatbot.messages), 1)
        self.assertEqual(
            self.chatbot.messages[0],
            {"role": "system", "content": "You are a helpful assistant."}
        )

    @patch('openai.ChatCompletion.create')
    def test_get_response_success(self, mock_create):
        """Test successful API response"""
        print("\nTesting successful response...")
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_create.return_value = mock_response

        async def run_test():
            response = await self.chatbot.get_response("Hello")
            print(f"Got response: {response}")
            self.assertEqual(response, "Test response")
            self.assertEqual(len(self.chatbot.messages), 3)
            
        asyncio.run(run_test())

    @patch('openai.ChatCompletion.create')
    def test_get_response_error(self, mock_create):
        """Test API error handling"""
        # Mock an API error
        mock_create.side_effect = Exception("API Error")

        async def run_test():
            response = await self.chatbot.get_response("Hello")
            self.assertEqual(response, "An error occurred: API Error")
            self.assertEqual(len(self.chatbot.messages), 2)  # system + user
            
        asyncio.run(run_test())

    async def interactive_chat(self):
        """Interactive chat session with the chatbot"""
        print("\nStarting interactive chat session (type 'quit' to exit)")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            response = await self.chatbot.get_response(user_input)
            print(f"\nChatbot: {response}")
            print("\nCurrent message history length:", len(self.chatbot.messages))

    def test_interactive(self):
        """Run an interactive chat session"""
        print("\nStarting interactive test...")
        asyncio.run(self.interactive_chat())

    @classmethod
    async def test_ai_response(cls):
        """Test getting a real response from the AI"""
        chatbot = Chatbot()
        response = await chatbot.get_response("What is the meaning of life?")
        print("\nAI Response:", response)
        return response

    @classmethod
    def test_run_ai_response(cls):
        """Run the AI response test"""
        print("\nTesting AI Response...")
        response = asyncio.run(cls.test_ai_response())
        return response

if __name__ == '__main__':
    response = TestChatbot.test_run_ai_response()
    print("\nTest completed!")