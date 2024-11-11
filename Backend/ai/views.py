from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_response import Chatbot
import json
import asyncio

chatbot = Chatbot()

@csrf_exempt
async def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Data: {data}")
            user_message = data.get('message')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            response = await chatbot.get_response(user_message)
            print(f"Response: {response}")
            return JsonResponse({'response': response})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
