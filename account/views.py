import json
import jwt
import re
import bcrypt
import requests

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models                    import User, Address , User_address
from foodly_project.my_settings import SECRET_KEY, ALGORITHM
from .utils                     import login_check

def find_special(name):
    return bool(re.search('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', name))

def email_check(email):
    return bool(re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

def find_space(string):
    return bool(re.search(' ', string))

class SignUpView(View):

    VALIDATION_RULES = {
        "email" : {
            "validator" : email_check,
            "message"   : "invalid email"  
        }, 
        "first_name" : {
            "validator" : find_special,
            "message"   : "invalid first name"  
        },
        ....
    }

    def post(self, request):
        data = json.loads(request.body)

        try:
            for field in data:
                rule = VALIDATION_RULES[field]
                if rule['validator'](data[field]):
                    return JsonResponse({"error" : rule['message']}, status=400)
    
            User(
                email      = data['email'],
                first_name = data['first_name'],
                last_name  = data['last_name'],
                password   = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()

            return JsonResponse({"message": "success"}, status=200)
        except ValidationError:
            return HttpResponse(status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_MISSING'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode(), user.password.encode('utf-8')):
                    token = jwt.encode({'email': data['email']}, SECRET_KEY['secret'],
                                       algorithm=ALGORITHM).decode()
                    return JsonResponse({'access': token}, status=200, content_type="application/json")

                return HttpResponse(status=401)
            return HttpResponse(status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)

class KakaoSignInView(View):
    def get(self, request):
        token = request.headers.get('Authorization', None)

        if token is None:
            return HttpResponse(status=400)

        try:
            url = 'https://kapi.kakao.com/v2/user/me'
            header = {"Authorization": f"Bearer {token}"}
            req = requests.get(url, headers=header)
            req_json = req.json()

            kakao_id = req_json.get('id', None)
            kakao_account = req_json.get('kakao_account', None)
            kakao_email = kakao_account.get('email', None)

            if User.objects.filter(email=kakao_email).exists():
                token = jwt.encode({"email": kakao_email}, SECRET_KEY['secret'], algorithm=ALGORITHM).decode("utf-8")
                return JsonResponse({"token": token}, status=200)

            User(
                email=kakao_email,
                kakao_id=kakao_id,
            ).save()

            token = jwt.encode({"email": kakao_email}, SECRET_KEY['secret'], algorithm=ALGORITHM).decode("utf-8")
            return JsonResponse({"token": token}, status=200)

        except KeyError:
            return HttpResponse(status=400)
        except jwt.DecodeError:
            return HttpResponse(status=401)


class AddressView(View):
    @login_check
    def post(self, request, address_id):
        address_data = json.loads(request.body)

        try:
            if address_data['first_name'] is None or address_data['last_name'] is None or address_data['company'] is None or \
                    address_data['address1'] is None or address_data['city'] is None or address_data['country'] is None or address_data['state'] is None:
                return HttpResponse(status=400)

            Address(
                first_name = address_data['first_name'],
                last_name  = address_data['last_name'],
                company    = address_data['company'],
                address1   = address_data['address1'],
                address2   = address_data.get('address2',None),
                city       = address_data['city'],
                country    = address_data['country'],
                state      = address_data['state']
            ).save()

            User_address(
                address_id = address_id,
                user_id = request.user.id
            ).save()

            return JsonResponse({'message':'success'} , status=200)
        except KeyError:
            return HttpResponse(status=400)
        except TypeError:
            return HttpResponse(status=400)
