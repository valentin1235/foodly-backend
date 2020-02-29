import jwt, bcrypt, json

from django.db    import IntegrityError
from django.views import View
from django.http  import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product

class ProductView(View):
    def get(self, request):
        products = Product.objects.select_related('harvest_year','measure')
        products_values = products.values(
                'name',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure', 
                'is_on_sale',
                'is_in_stock',
        )
        return JsonResponse({'data' : list(products_values)}, status = 200)

class ProductDetailView(View):
    def get(self, request, slug):
        product_info = Product.objects.filter(name=slug).values(
                'name', 
                'harvest_year_id__year', 
                'is_in_stock', 
                'measure_id__measure', 
                'description', 
                'price', 
                'small_image', 
                'big_image', 
                'energy', 
                'carbonydrate', 
                'protein', 
                'fat', 
                'mineral', 
                'vitamin'
        )
        similar_product = Product.objects.filter(name=slug).values(
                'similar_product__name', 
                'similar_product__harvest_year_id__year', 
                'similar_product__is_in_stock', 
                'similar_product__measure_id__measure'
        )
        return JsonResponse({'data' : {'product_info' : list(product_info), 'similar_product' : list(similar_product)}}, status = 200)
        
