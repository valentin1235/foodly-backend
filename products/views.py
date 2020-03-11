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
        sort_by  = request.GET.get('sort_by', 'id')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 12))

        product_info = (
            Product
            .objects
            .select_related('harvest_year', 'measure')
            .order_by(sort_by)
            .values(
                'name',
                'id',
                'price',
                'small_image',
                'harvest_year__year',
                'measure_id__measure',
                'is_on_sale',
                'is_in_stock',
            )[offset:limit]
        )

        return JsonResponse({'data' : list(product_info)}, status = 200)

class ProductDetailView(View):
    def get(self, request, product_id):
        product_info = (
            Product
            .objects
            .select_related('measure', 'harvest_year')
            .prefetch_related('similar_product')
            .get(id=product_id)
        )

        similiar_products = list(
            product_info
            .similar_product
            .values(
                'name', 
                'harvest_year_id__year', 
                'is_in_stock', 
                'measure_id__measure'
            )
        )

        product_info = {
            'id'                    : product_info.id,
            'name'                  : product_info.name,
            'harvest_year_id__year' : product_info.harvest_year.year,
            'measure_id__measure'   : product_info.measure.measure,
            'is_in_stock'           : product_info.is_in_stock,
            'description'           : product_info.description, 
            'price'                 : product_info.price, 
            'small_image'           : product_info.small_image, 
            'big_image1'            : product_info.big_image1, 
            'big_image2'            : product_info.big_image2,
            'big_image3'            : product_info.big_image3,
            'energy'                : product_info.energy, 
            'carbonydrate'          : product_info.carbonydrate, 
            'protein'               : product_info.protein, 
            'fat'                   : product_info.fat, 
            'mineral'               : product_info.mineral, 
            'vitamin'               : product_info.vitamin,
            'similar_product'       : similiar_products
        }
        
        return JsonResponse({'data' : product_info}, status = 200)

class ProductCategoryView(View):
    def get(self, request, category_name):
		sort_by = request.GET.get('sort_by', 'id')
		offset  = int(request.GET.get('offset', 0))
		limit   = int(request.GET.get('limit', 12))

		categorized_page = (
			Product
			.objects
			.prefetch_related('harvest_year', 'measure')
			.filter(category__name = category_name)
			.order_by(sort_by)
			.values(
				'id',
				'name',
				'price',
				'small_image',
				'harvest_year__year',
				'measure_id__measure',
				'is_on_sale',
				'is_in_stock',
			)[offset:limit]
		)
        
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
        )[offset:limit]
        
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
		bundle_info = [{
			"title"           : bundle.title,
			"price"           : bundle.price,
			"is_in_promotion" : bundle.is_in_promotion,
			"content_info"    : [
				"measure" : data.product_set.measure.measure,
				"name"    : data.product_set.name,
				"qty"	  : data.qty
			] for data in bundle
		} for bundle for Bundle.objects.prefetch_related('product_set')]

        return JsonResponse({'data' :  bundle_info}, status = 200)

class RecommendationView(View):
    def get(self, request):
        data_caching       = Recipe.objects.prefetch_related('product_set').get(is_main = True)
        recommended_recipe = {
                'title'         : data_caching.title,
                'thumbnail_url' : data_caching.thumbnail_url,
                'product_info'  : list(data_caching.product_set.values(
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
					'recipe':[{
						'id':recipe.id,
						'title':recipe.title,
						'ingredient':recipe.ingredient,
						'description':recipe.description,
						'thumbnail_url':recipe.thumbnail_url,
					} for recipe in recipe_data]
				}

            return JsonResponse({'data':data},status=200)

		return JsonResponse({"error" : "invalid keyword"}, status=400)


