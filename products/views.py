import jwt, bcrypt, json

from django.db import IntegrityError
from django.db.models import Q
from django.views import View
from django.http import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product


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


from django.db import IntegrityError
from django.db.models import Count
from django.views import View
from django.http import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product, Category, ProductCategory, Recipe, Bundle, ProductBundle


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

        if sort_by:
            sort = product_info.order_by(sort_by)

            return JsonResponse({'data': list(sort)}, status=200)

        return JsonResponse({'data': list(product_info)}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):
        data_caching = Product.objects.select_related('measure', 'harvest_year').prefetch_related(
            'similar_product').get(id=product_id)
        product_info = {
            'name': data_caching.name,
            'harvest_year_id__year': data_caching.harvest_year.year,
            'measure_id__measure': data_caching.measure.measure,
            'is_in_stock': data_caching.is_in_stock,
            'description': data_caching.description,
            'price': data_caching.price,
            'small_image': data_caching.small_image,
            'big_image1': data_caching.big_image1,
            'big_image2': data_caching.big_image2,
            'big_image3': data_caching.big_image3,
            'energy': data_caching.energy,
            'carbonydrate': data_caching.carbonydrate,
            'protein': data_caching.protein,
            'fat': data_caching.fat,
            'mineral': data_caching.mineral,
            'vitamin': data_caching.vitamin,
            'similar_product': list(data_caching.similar_product.values('name', 'harvest_year_id__year', 'is_in_stock',
                                                                        'measure_id__measure'))
        }

        return JsonResponse({'data': product_info}, status=200)


class ProductCategoryView(View):
    def get(self, request, category_name):
        sort_by = request.GET.get('sort_by', None)
        category_filter = Product.objects.filter(category__name=category_name).prefetch_related('harvest_year',
                                                                                                'measure')
        categorized_page = category_filter.values(
            'name',
            'price',
            'small_image',
            'harvest_year__year',
            'measure_id__measure',
            'is_on_sale',
            'is_in_stock',
        )

        if sort_by:
            sort = categorized_page.order_by(sort_by)

            return JsonResponse({'data': list(sort)}, status=200)

        return JsonResponse({'data': list(categorized_page)}, status=200)


class RecipeView(View):
    def get(self, request):
        recipe_info = Recipe.objects.values(
            'title',
            'description',
            'company',
            'thumbnail_url',
            'posting_date'
        )

        return JsonResponse({'data': list(recipe_info)}, status=200)


class RecipeDetailView(View):
    def get(self, request, recipe_id):
        recipe_detail = Recipe.objects.filter(id=recipe_id).values(
            'title',
            'posting_date',
            'company',
            'author',
            'description',
            'ingredient',
            'direction'
        )

        return JsonResponse({'data': list(recipe_detail)}, status=200)


class BundleView(View):
    def get(self, request):
        data_caching = Bundle.objects.prefetch_related('product_set')
        bundle_info = data_caching.values('title', 'price', 'is_in_promotion')
        content_info = [
            list(data.product_set.values('measure_id__measure', 'name')
                 .annotate(Count('name'))) for data in data_caching
        ]
        bundle = [data for data in zip(bundle_info, content_info)]

        return JsonResponse({'data': bundle}, status=200)


class SearchView(View):

    def get(self, request):
        query = request.GET.get('search', None)

        if len(query) > 2:
            # 검색을 한다 . query 를 받는다 left 니깐. 
            # query 가 포함되어있는 product 를 받고 , 참조하고 있는 harvest_year에 대한 내용도 가져와야한다.
            recipe_data = Recipe.objects.filter(Q(title__icontains=query))
            print('qweqwe' , recipe_data)
#            product_data = Product.objects.filter(Q(name__icontains=query)).select_related('harvest_year').get(id=3).harvest_year.year
            product_data = Product.objects.filter(Q(name__icontains=query)).select_related('harvest_year')
            print('asdfasdf' ,product_data)
            harvet = product_data.get(id=3).harvest_year.year
            print('asdfasdfasdfasdf',harvet)


#            data={'product':[{
#                'id' : product['id'],
#                'name':product['name'],
#                'price':product['price'],
#                'description':product['description'],
#                'small_image':product['small_image'],
#                'harvest_year':product[''],
##                'harvest_year':Product.objects.select_related('harvest_year').get(id=product['harvest_year_id']).harvest_year.year,
#                'is_in_stock':product['is_in_stock'],
#                }for product in product_data.values()],
#                'recipe':[{
#                'id':recipe['id'],
#                'title':recipe['title'],
#                'ingredient':recipe['ingredient'],
#                'description':recipe['description'],
#                'thumbnail_url':recipe['thumbnail_url'],
#            }for recipe in recipe_data.values()]}

            return HttpResponse(status=200)

