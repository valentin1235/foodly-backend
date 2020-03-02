import json
import jwt
import re
import bcrypt

from .models import Review

from products.models import Product
from account.models import User
from django.views import View
from django.http import HttpResponse, JsonResponse
from account.utils import login_check


class ReviewCreateView(View):
    def get(self, request):  # read
        review_list = Review.objects.all()
        return JsonResponse({"review": list(review_list)}, status=200)

    @login_check
    def post(self, request, product_id):  # create
        data = json.loads(request.body)
        user_id = request.user.id
        try:
            if Product.objects.filter(id=product_id).exists():
                Review(
                    user_id=user_id,
                    review=data['review'],
                    product_id=product_id
                ).save()

                review_data = Review.objects.all()
                return JsonResponse({'message': list(review_data)}, status=200)

        except KeyError:
            return HttpResponse(status=400)
        except User.DoesNotExist:
            return HttpResponse(status=400)

    def get(self, request):
        review_data = Review.objects.all()
        return JsonResponse({'review': list(review_data)}, status=200)


class ReviewUpdateView(View):
    @login_check
    def post(self, request):
        return

    def get(self, request):
        review_data = Review.objects.all()
        return JsonResponse({'review': list(review_data)}, status=200)


class ReviewDeleteView(View):
    @login_check
    def post(self, request):
        return

    def get(self, request):
        review_data = Review.objects.all()
        return JsonResponse({'review': list(review_data)}, status=200)
