import json
import os
import requests
from django.http import HttpResponse,JsonResponse
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt

# Load environment variables from .env file
load_dotenv()



MLModel_server_URL = "http://127.0.0.1:5000"
MLModel_server_API_Key = os.getenv('ML_Server_API_KEY')


@csrf_exempt  # Use csrf_exempt To disable csrf token during test and development but must be deleted in production
#predict chat
def get_chat_response(request):

    if request.method=="POST":
        data = json.loads(request.body)

        if 'query' not in data or not data['query']:
            return JsonResponse({'error': 'Query parameter "query" is required and cannot be empty.'}, status=400)


        chat_url = MLModel_server_URL+"/api/process_chat"
        # Date to be sent to Flask server
        data = {
            'query': data.get('query')
        }

        # Headers to authenticate server
        headers = {
            'MY-API-KEY': MLModel_server_API_Key
        }

        try:
            response = requests.post(chat_url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                # Handle user History here
                return HttpResponse(response_data.get('response'))

            else:
                return HttpResponse(f"Error accessing Flask API {response_data.get('error')} - Status Code: {response.status_code}")

        # Error reaching the destination
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error accessing Flask API: {str(e)}")
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)





