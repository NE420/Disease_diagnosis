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
    #Accepts only Post Reeuests
    if request.method=="POST":
        #Get The Body data of the request
        data = json.loads(request.body)

        #Make sure that there exists a key named query and it has a value
        if 'query' not in data or not data['query']:
            return JsonResponse({'error': 'Query parameter "query" is required and cannot be empty.'}, status=400)

        #URL of Flask api that accepts chat queries
        chat_url = MLModel_server_URL+"/api/process_chat"
        # Date to be sent to Flask server must be in json form
        data = {
            'query': data.get('query')
        }

        # Headers to authenticate flask server
        headers = {
            'MY-API-KEY': MLModel_server_API_Key
        }

        try:
            #send query and get response
            response = requests.post(chat_url, json=data, headers=headers)
            response_data = response.json() #cast to a dictionary

            #Operation success
            if response.status_code == 200:
                # Handle user History here
                return HttpResponse(response_data.get('response'))

            else:
                return HttpResponse(f"Error accessing Flask API {response_data.get('error')} - Status Code: {response.status_code}",status= response.status_code)

        # Error reaching flask
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error accessing Flask API: {str(e)}")
    else:

        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)




#View to classify images by sending image to flask model
@csrf_exempt  # Use csrf_exempt to disable CSRF token requirement (for development/testing)
def process_image(request):
    #Accepts only Post Methods
    if request.method == 'POST':
        # Check if request contains a file
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part in the request'}, status=400)
        #Retrieve the file
        file = request.FILES['file']

        # Check if file name is empty
        if file.name == '':
            return JsonResponse({'error': 'No file selected for uploading'}, status=400)

        # Check if file type is allowed
        if file and allowed_file(file.name):
            try:
                # Prepare data to send to Flask server as a form files
                files = {
                    'file': file
                }

                # URL on Flask server for image processing
                image_url = MLModel_server_URL + "/api/process_image"

                # Headers with API key for authentication
                headers = {
                    'MY-API-KEY': MLModel_server_API_Key
                }

                try:
                    # Send POST request to Flask server
                    response = requests.post(image_url, files=files, headers=headers)

                    # Handle response from Flask server
                    if response.status_code == 200:
                        return JsonResponse(response.json(), status=200)
                    else:
                        return HttpResponse(f"Error accessing Flask API {response.json().get('error')} - Status Code: {response.status_code}", status=response.status_code)

                except requests.exceptions.RequestException as e:
                    return HttpResponse(f"Error accessing Flask API: {str(e)}", status=500)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else:
            return JsonResponse({'error': 'Allowed file types are png, jpg, jpeg'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# function to check if the file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
