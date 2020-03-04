import jwt, bcrypt, json

from django.db import IntegrityError
from django.db.models import Q
from django.views import View
from django.http import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product, Recipe


# from recipes.models import Recipes
# from .utils  import login_required

class ProductView(View):
    def get(self, request):
        products = Product.objects.select_related('harvest_year', 'measure', 'color', 'wood_type')
        products_values = products.values(
            'name',
            'price',
            'thumbnail_url',
            'harvest_year__year',
            'measure_id__measure',
            'is_on_sale', 'is_in_stock',
            'color_id__name',
            'wood_type_id__name'
        )
        return JsonResponse({'data': list(products_values)}, status=200)


class SearchView(View):

    def get(self, request):
        data = request.GET.get('search', None)

        try:
            if len(data) > 2:
                recipe_data = list(Recipe.objects.values().filter(Q(title__icontains=data)))
                product_data = list(Product.objects.values().filter(Q(name__icontains=data)))
                return JsonResponse({"SUCCESS": f'recipe_data : {recipe_data} + product_data : {product_data}'},
                                    status=200)

        except:
            return HttpResponse(status=400)
