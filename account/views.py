import json, jwt
import bcrypt
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Account
from my_settings import SECRET_KEY


# Create your views here.

class AccountView(View):  # 회원가입

    def post(self, request):
        data = json.loads(request.body)
        if Account.objects.filter(email=data['email']).exists():
            return JsonResponse({'email': '존재하는 이메일 입니다.'}, status=200)

        if data['password'] is None or data.get('password', None):
            return JsonResponse({'password': 'password 를 입력하세요.'}, status=200)

        Account(
            email=data['email'],
            name=data['name'],
            gender=data['gender'],
            password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        ).save()

        return HttpResponse(status=200)


class LoginView(View):

    def post(self, request):
        data = json.load(request.body)
        print(data)
        try:
            if Account.objects.filter(email=data['email']).exists():
                user = Account.objects.get(email=data['email'])
                if bcrypt.checkpw(data['password'].encode(), user.password.encode('utf-8')):
                    token = jwt.encode({'email': data['email']}, SECRET_KEY, algorithm='HS256').decode()
                    return JsonResponse({'access': token}, status=200, content_type="application/json")
                return HttpResponse(status=401)
            return HttpResponse(status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
