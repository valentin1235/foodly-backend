import jwt, bcrypt, json

from django.db        import IntegrityError
from django.db.models import Count, Q
from django.views     import View
from django.http      import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models                    import (
        Product, 
        Category, 
        ProductCategory, 
        Recipe, 
        Bundle, 
        ProductBundle
)

class ProductView(View):
    def get(self, request):
        sort_by = request.GET.get('sort_by', 'id')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 12))
        product_info = Product.objects.select_related('harvest_year', 'measure').order_by(sort_by).values(
                'name',
                'id',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure',
                'is_on_sale',
                'is_in_stock',
        )[offset:offset+limit]

        return JsonResponse({'data' : list(product_info)}, status = 200)

class ProductDetailView(View):
    def get(self, request, product_id):
        data_caching = (
                Product.objects
                .select_related('measure', 'harvest_year')
                .prefetch_related('similar_product')
                .get(id=product_id)
        )
        product_info = {
                'id'                    : data_caching.id,
                'name'                  : data_caching.name,
                'harvest_year_id__year' : data_caching.harvest_year.year,
                'measure_id__measure'   : data_caching.measure.measure,
                'is_in_stock'           : data_caching.is_in_stock,
                'description'           : data_caching.description, 
                'price'                 : data_caching.price, 
                'small_image'           : data_caching.small_image, 
                'big_image1'            : data_caching.big_image1, 
                'big_image2'            : data_caching.big_image2,
                'big_image3'            : data_caching.big_image3,
                'energy'                : data_caching.energy, 
                'carbonydrate'          : data_caching.carbonydrate, 
                'protein'               : data_caching.protein, 
                'fat'                   : data_caching.fat, 
                'mineral'               : data_caching.mineral, 
                'vitamin'               : data_caching.vitamin,
                'similar_product'       : list(data_caching.similar_product.values('name', 'harvest_year_id__year', 'is_in_stock', 'measure_id__measure'))
                }
        
        return JsonResponse({'data' : product_info}, status = 200)

class ProductCategoryView(View):
    def get(self, request, category_name):
        sort_by = request.GET.get('sort_by', 'id')
        category_filter = Product.objects.prefetch_related('harvest_year', 'measure').filter(category__name = category_name)        
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 12))        
        categorized_page = category_filter.order_by(sort_by).values(
                'id',
                'name',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure',
                'is_on_sale',
                'is_in_stock',
        )[offset:offset+limit]
        
        return JsonResponse({'data' : list(categorized_page)}, status = 200)

class RecipeView(View):
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 12))
        recipe_info = Recipe.objects.order_by('id').values(
                'id',
                'title', 
                'description', 
                'company', 
                'thumbnail_url',
                'posting_date'
        )[offset:offset+limit]
        
        return JsonResponse({'data' : list(recipe_info)}, status = 200)

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
        
        return JsonResponse({'data' : list(recipe_detail)}, status = 200)

class BundleView(View):
    def get(self, request):
        bundles      = Bundle.objects.prefetch_related('product_set')
        content_info = [
                list(data.product_set.values('measure_id__measure', 'name')
                    .annotate(Count('name'))) for data in bundles
        ]
        bundle_info  = [{
            'title'            : bundle.title, 
            'price'            : bundle.price, 
            'is_in_promomtion' : bundle.is_in_promotion,
            'content_info'     : content_info} 
            for bundle in bundles]

        return JsonResponse({'data' :  bundle_info}, status = 200)

class RecommendationView(View):
    def get(self, request):
        recipe = Recipe.objects.prefetch_related('product_set').get(is_main = True)
        recommended_recipe = {
                'title'         : recipe.title,
                'thumbnail_url' : recipe.thumbnail_url,
                'product_info'  : list(recipe.product_set.values(
                    'name',
                    'price',
                    'measure_id__measure',
                    'small_image',
                    'measure_id__measure',
                    'harvest_year_id__year'
                ))
        }

        return JsonResponse({'data' : recommended_recipe}, status = 200)

class SearchView(View):

    def get(self, request):
        query = request.GET.get('keyword', None)

        if len(query) > 2:
            recipe_data  = Recipe.objects.filter(Q(title__icontains=query)).all()
            product_data = Product.objects.filter(Q(name__icontains=query)).select_related('harvest_year').all()

            data={
					'product':[{
						'id'           : product.id,
						'name'         : product.name,
						'price'        : product.price,
						'description'  : product.description,
						'small_image'  : product.small_image,
						'harvest_year' : product.harvest_year.year,
					} for product in product_data],
					'recipe'            : [{
						'id'            : recipe.id,
						'title'         : recipe.title,
						'ingredient'    : recipe.ingredient,
						'description'   : recipe.description,
						'thumbnail_url' : recipe.thumbnail_url,
					} for recipe in recipe_data]
				}

            return JsonResponse({'data':data},status=200)

		return JsonResponse({"error" : "invalid keyword"}, status=400)
