import json, requests
import jwt
import re
import bcrypt
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
        try:
            data = json.loads(request.body)
            validate_email(data['email'])
            print('data : ', data)

            if data['email'] is None or data['first_name'] is None or data['last_name'] is None or data[
                'password'] is None:
                return JsonResponse({'message': 'NOT_VALID'}, status=400)

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
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()

            return JsonResponse({"message": "success"}, status=200)

        except ValidationError:
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse(status=400)

    def get(self, request):
        return JsonResponse({"message": "회원가입페이지"}, status=200)


class SignInView(View):
    @login_check
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
            return JsonResponse({"message": "INVALID_USER"}, status=401)


class AddressCreateView(View):
    @login_check
    def post(self, request):
        address_data = json.loads(request.body)
        print(address_data)
        return

    def get(self, request):
        address_data = Address.objects.all()
        return JsonResponse({"message": list(address_data)}, status=200)


class AddressUpdateView(View):
    @login_check
    def post(self, request, address_id):
        address_data = json.loads(request.body)
        print(address_data)

        if address_data['first_name'] is None \
                or address_data['last_name'] is None \
                or address_data['address1'] is None \
                or address_data['city'] is None \
                or address_data['country'] is None:
            return JsonResponse({"message": "INVALD_DATA"}, status=400)

        if find_special(address_data['first_name']) or find_special(address_data['last_name']):
            return HttpResponse(status=400)

        Address(

        ).save()

        return JsonResponse({"message": "SUCCESS"}, status=200)

    def delete(self, request, address_id):
        return


class KakaoLoginView(View):
    def get(self, request):
        try:
            data = request.GET.get('Authorization', None)
            print(data)
            if data:
                api_key = '55c0f58206b61a1d088d119aaed7e553'
                redirect_uri = 'http://localhost:8000'
                response_return = f'/oauth/authorize?client_id={api_key}&redirect_uri={redirect_uri}&response_type={data}'
                return JsonResponse({'message': f'{response_return}'}, status=200)
        except:
            return HttpResponse(status=400)
