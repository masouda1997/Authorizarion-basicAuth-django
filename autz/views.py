import json
import base64
import requests
from django.http import HttpResponse , JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

@csrf_exempt
def test(request):
    username = 'masoud'
    password = 'masouda30376'
    # Encode the username and password in Base64
    auth_string = f'{username}:{password}'
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode('utf-8')
    # Set the Authorization header with the Basic authentication scheme
    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }
    # Send a request with the headers
    response = requests.get('http://127.0.0.1:8000/api/aut/', headers=headers)
    # Process the response
    if response.status_code == 200:
        # Retrieve the data from the response and parse it as JSON
        data = response.json()
        # Convert the data to a JSON string
        json_data = json.dumps(data)
        # Return the JSON response
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponse('Failure!', content_type='text/plain')
    

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            authorization_header = request.headers.get('Authorization' ,'')
            print("🔴",authorization_header)
            _,encode_creadentials = authorization_header.split(' ')
            decode_credentials = base64.b64decode(encode_creadentials).decode('utf-8')
            username,password = decode_credentials.split(':')
            print(username , password)
            user = authenticate(request , username=username , password = password)
            if user is not None:
                # token = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    'email':user.email,
                    'username':user.username,
                    # "password":token.password
                    },safe=False)
            return JsonResponse({"error ":"login failed"}, status=401)
        except Exception as e :
            return JsonResponse({"error " : str(e)}, status=500)
    return JsonResponse({'error':'method not allowes'} , status=405)