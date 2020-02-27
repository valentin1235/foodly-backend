import json, jwt, re, bcrypt
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User


# Create your views here.
def find_special(name):
    return bool(re.search('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', name))


def find_gongbeak(string):
    return bool(re.search(' ', string))


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            validate_email(data['email'])

            if User.objects.filter(email=data['email']).exists():
                return HttpResponse(status=409)

            if True is find_special(data['first_name']):
                return HttpResponse(status=409)
            if True is find_special(data['last_name']):
                return HttpResponse(status=409)

            if True is find_gongbeak(data['password']):
                return HttpResponse(status=400)

            if len(data["password"]) < 6:
                return JsonResponse({"message": "비밀번호 짦음"}, status=400)

            User(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()

        except ValidationError:
            return HttpResponse(status=401)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                if bcrypt.checkpw(data['password'].encode(), user.password.encode('utf-8')):  # 특정값을 가지고 와야한다.
                    token = jwt.encode({'email': data['email']}, "6기화이팅", algorithm='HS256').decode()
                    return JsonResponse({'access': token}, status=200, content_type="application/json")
                return HttpResponse(status=401)
            return HttpResponse(status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

    def get(self, request):
        return JsonResponse({'message': '로그인 페이지입니다.'}, status=200)
