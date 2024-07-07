import json
import os
import requests
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Disease_Diagnosis import models
from Disease_Diagnosis.models import ChatSession, Interaction

# Load environment variables from .env file
load_dotenv()



MLModel_server_URL = "http://127.0.0.1:5000"
MLModel_server_API_Key = os.getenv('ML_Server_API_KEY')

class ProcessChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # Accepts only Post Reeuests
        if request.method == "POST":
            # Get The Body data of the request
            data = json.loads(request.body)

            # Make sure that there exists a key named query and it has a value
            if 'query' not in data or not data['query']:
                return JsonResponse({'error': 'Query parameter "query" is required and cannot be empty.'}, status=400)

            if 'chat_id' not in data or not data['chat_id']:
                return JsonResponse({'error': 'Query parameter "chat_id" is required and cannot be empty.'}, status=400)
            query = data.get('query')
            chat_id = data.get('chat_id')

            chat_session = ChatSession.objects.get(id=chat_id)
            if chat_session.user != request.user:#make sure the request user is the same as chat user
                raise PermissionDenied("You are not allowed to add interactions to this session.")

            #retrieve previous Interactions for context
            interactions = Interaction.objects.filter(chat_session=chat_session).order_by('timestamp')
            context = ""

            for interaction in interactions:
                context+= f"<|start_header_id|>user<|end_header_id|>{interaction.user_question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>{interaction.model_answer}<|eot_id|>"

            question = f'{context} <|start_header_id|>user<|end_header_id|>{data["query"]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'.strip()


            # URL of Flask api that accepts chat queries
            #chat_url = MLModel_server_URL + "/api/process_chat"
            chat_url = "https://b76a-34-67-11-26.ngrok-free.app"
            # Date to be sent to Flask server must be in json form
            data = {
                'query': question
            }

            # Headers to authenticate flask server
            headers = {
                'MY-API-KEY': MLModel_server_API_Key
            }
            print(question)
            try:
                # send query and get response
                response = requests.post(chat_url, json=data, headers=headers)
                response_data = response.json()  # cast to a dictionary

                # Operation success
                if response.status_code == 200:

                    chat_session = ChatSession.objects.get(id=chat_id)
                    #Create new interactio
                    Interaction.objects.create(
                        chat_session=chat_session,
                        user_question=query,
                        model_answer=response_data.get('response')
                    )

                    return HttpResponse(response_data.get('response'))

                else:
                    return HttpResponse(
                        f"Error accessing Flask API {response_data.get('error')} - Status Code: {response.status_code}",
                        status=response.status_code)

            # Error reaching flask
            except requests.exceptions.RequestException as e:
                return HttpResponse(f"Error accessing Flask API: {str(e)}")
        else:

            return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


#View to classify images by sending image to flask model
class ProcessImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):

        # Accepts only Post Methods
        if request.method == 'POST':

            # Get the User object using the username
            username = request.user.username

            # Get the User object using the username
            user_id = get_object_or_404(User, username=username).id

            user_info = get_object_or_404(models.UserInfo, user_id=user_id)

            gender = user_info.gender
            if(gender=='M'):
                gender = 'male'
            elif gender=='F':
                gender = 'female'
            age = user_info.age

            data = request.data #Access form attributes

            img_pos = data.get('position')

            # validate image position in the body
            if img_pos is None:
                return JsonResponse({'error': 'Json value "position" is required and cannot be empty.'}, status=400)
            if img_pos not in ['head/neck', 'lower extremity', 'oral/genital', 'palms/soles', 'torso',
                               'upper extremity']:
                return JsonResponse({'error': 'Json value "position" is not a valid poition.'}, status=400)

            # Check if request contains a file
            if 'file' not in request.FILES:
                return JsonResponse({'error': 'No file part in the request'}, status=400)
            # Retrieve the file
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
                    # Meta data required by image classifier model
                    req_data = {

                        'position': img_pos,
                        'gender': gender,
                        'age': age
                    }
                    # URL on Flask server for image processing
                    #image_url = MLModel_server_URL + "/api/process_image"
                    image_url = "https://33bf-41-44-140-48.ngrok-free.app"+"/api/"
                    # Headers with API key for authentication
                    headers = {
                        'MY-API-KEY': MLModel_server_API_Key
                    }

                    try:
                        # Send POST request to Flask server
                        response = requests.post(image_url, data=req_data, files=files, headers=headers)

                        # Handle response from Flask server
                        if response.status_code == 200:
                            return JsonResponse(response.json(), status=200)
                        else:
                            return HttpResponse(
                                f"Error accessing Flask API {response.json().get('error')} - Status Code: {response.status_code}",
                                status=response.status_code)

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
