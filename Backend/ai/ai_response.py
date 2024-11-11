import openai
import os
import dotenv
from typing import List, Dict
from openai import AsyncOpenAI
import asyncio

dotenv.load_dotenv()

class Chatbot:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    async def get_response(self, user_message: str) -> str:
        # Add user message to conversation history
        self.messages.append({"role": "user", "content": user_message})
        
        try:
            # Create chat completion using new API format
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Updated model name
                messages=self.messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract assistant's response (updated format)
            assistant_response = response.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def clear_history(self):
        """Reset the conversation history"""
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        
if __name__ == "__main__":
    async def main():
        chatbot = Chatbot()
        response = await chatbot.get_response("Hello, how are you?")
        print(response)

    asyncio.run(main())
