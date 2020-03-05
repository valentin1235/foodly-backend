import json
import jwt
import re
import bcrypt
import requests

from .models import User, Address

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from foodly_project.my_settings import SECRET_KEY, ALGORITHM
from .utils import login_check


# Create your views here.
def find_special(name):
    return bool(re.search('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', name))


def find_space(string):
    return bool(re.search(' ', string))


class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data['email'])

            if data['email'] is None or data['first_name'] is None or data['last_name'] is None or data[
                'password'] is None:
                return JsonResponse({'message': 'NOT_VALID'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return HttpResponse(status=400)

            if find_special(data['first_name']):
                return HttpResponse(status=400)

            if find_special(data['last_name']):
                return HttpResponse(status=400)

            if find_space(data['password']):
                return HttpResponse(status=400)

            if len(data["password"]) < 6:
                return JsonResponse({"message": "비밀번호 짦음"}, status=400)

            User(
                email=data['email'],
                first_name =data['first_name'],
                last_name=data['last_name'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()

            return JsonResponse({"message": "success"}, status=200)

        except ValidationError:
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse(status=400)


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

        try:
            url = 'https://kapi.kakao.com/v2/user/me'
            header = {"Authorization": f"Bearer {token}"}
            req = requests.get(url, headers=header)
            req_json = req.json()

            kakao_id = req_json.get('id', None)
            kakao_account = req_json.get('kakao_account')
            kakao_email = kakao_account.get('email', None)

            if User.objects.filter(email=kakao_email).exists():
                token = jwt.encode({"email": kakao_email}, SECRET_KEY['secret'], algorithm=ALGORITHM).decode(
                    "utf-8")
                return JsonResponse({"token": token}, status=200)

            User(
                email=kakao_email,
                kakao_id=kakao_id,
            ).save()

            token = jwt.encode({"email": kakao_email}, SECRET_KEY['secret'], algorithm=ALGORITHM).decode(
                "utf-8")
            return JsonResponse({"token": token}, status=200)

        except TypeError:
            return HttpResponse(status=400)

        except jwt.DecodeError:
            return HttpResponse(status=400)

