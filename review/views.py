import json
from .models import Review

from products.models import Product
from account.models import User
from django.views import View
from django.http import HttpResponse, JsonResponse
from account.utils import login_check


class ReviewView(View):
    @login_check
    def post(self, request, product_name):
        data = json.loads(request.body)
        review = data.get('review', None)
        try:
            if Product.objects.filter(name=product_name).exists():
                if review:
                    Review(
                        user_id=request.user.id,
                        review=review,
                        product_id=Product.objects.get(name=product_name).id
                    ).save()

                    return JsonResponse({'message': "SUCCESS"}, status=200)

        except KeyError:
            return HttpResponse(status=400)

        except User.DoesNotExist:
            return HttpResponse(status=400)

    @login_check
    def get(self, request, product_name):

        try:

            if Product.objects.filter(name=product_name).exists():
                product_id = Product.objects.get(name=product_name).id
                review_data = Review.objects.filter(product_id=product_id).values()
            return JsonResponse({"message": f"{review_data}"}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message": 'INVALD_PRODUCT'}, status=400)


class ReviewDetailView(View):
    @login_check
    def post(self, request, product_name, review_id):
        data = json.loads(request.body)
        review = data.get('review', None)
        product_id = Product.objects.get(name=product_name).id

        try:
            review_data = Review.objects.get(id=review_id, product_id=product_id, user_id=request.user.id)

            if review:
                review_data.review = data['review']
                review_data.save()
                review_data = Review.objects.values()
                return JsonResponse({'message': list(review_data)}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({'message': 'INVALD_REVIEW'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALD_USER"}, status=400)

    @login_check
    def delete(self, request, product_name, review_id):
        product_id = Product.objects.get(name=product_name).id

        try:
            review_data = Review.objects.get(id=review_id, user_id=request.user.id, product_id=product_id)
            review_data.delete()
            review_data = Review.objects.values()
            return JsonResponse({"SECCESS": list(review_data)}, status=200)

        except Product.DoesNotExist:
            return HttpResponse({"message": "INVALD_REVIEW"}, status=400)
