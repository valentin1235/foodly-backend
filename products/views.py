import jwt, bcrypt, json

from django.db    import IntegrityError
from django.views import View
from django.http  import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product, Category, ProductCategory, Recipe

class ProductView(View):
    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get('sort_by', None)
        product_info = Product.objects.select_related('harvest_year', 'measure').values(
                'name',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure', 
                'is_on_sale',
                'is_in_stock',
        )

        if sort_by == 'title-ascending':
            name_ascending = product_info.order_by('name')
            return JsonResponse({'data' : list(name_ascending)}, status = 200)
        
        elif sort_by == 'title-descending':
            name_descending = product_info.order_by('-name')
            return JsonResponse({'data' : list(name_descending)}, status = 200)

        elif sort_by == 'price-ascending':
            price_ascending = product_info.order_by('price')
            return JsonResponse({'data' : list(price_ascending)}, status = 200)

        elif sort_by == 'price-descending':
            price_descending = product_info.order_by('-price')
            return JsonResponse({'data' : list(price_descending)}, status = 200)

        return JsonResponse({'data' : list(product_info)}, status = 200)

class ProductDetailView(View):
    def get(self, request, slug):
        product_info = Product.objects.filter(name=slug).select_related('measure', 'harvest_year').values(
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
        similar_product = Product.objects.filter(name=slug).select_related('from_product', 'to_product').values(
                'similar_product__name', 
                'similar_product__harvest_year_id__year', 
                'similar_product__is_in_stock', 
                'similar_product__measure_id__measure'
        )
        return JsonResponse({'data' : {'product_info' : list(product_info), 'similar_product' : list(similar_product)}}, status = 200)
        
class ProductCategoryView(View):
    def get(self, request, slug):
        sort_by = request.GET.get('sort_by', None)
        category_filter = Product.objects.filter(category__name = slug).prefetch_related('harvest_year', 'measure')
        categorized_page = category_filter.values(
                'name',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure',
                'is_on_sale',
                'is_in_stock',
        )

        if sort_by == 'title-ascending':
            name_ascending = categorized_page.order_by('name')
            return JsonResponse({'data' : list(name_ascending)}, status = 200)

        elif sort_by == 'title-descending':
            name_descending = categorized_page.order_by('-name')
            return JsonResponse({'data' : list(name_descending)}, status = 200)

        elif sort_by == 'price-ascending':
            price_ascending = categorized_page.order_by('price')
            return JsonResponse({'data' : list(price_ascending)}, status = 200)

        elif sort_by == 'price-descending':
            price_descending = categorized_page.order_by('-price')
            return JsonResponse({'data' : list(price_descending)}, status = 200)

        return JsonResponse({'data' : list(categorized_page)}, status = 200)

class RecipeView(View):
    def get(self, request):
        recipe_info = Recipe.objects.values(
                'title', 
                'description', 
                'company', 
                'thumbnail_url',
                'posting_date'
        )
        return JsonResponse({'data' : list(recipe_info)}, status = 200)

class RecipeDetailView(View):
    def get(self, request, int):
        recipe_detail = Recipe.objects.filter(id=int).values(
                'title', 
                'posting_date', 
                'company', 
                'author', 
                'description', 
                'ingredient', 
                'direction'
        )
        return JsonResponse({'data' : list(recipe_detail)}, status = 200)
