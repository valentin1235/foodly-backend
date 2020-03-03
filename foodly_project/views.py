import json

from django.db    import IntegrityError
from django.views import View
from django.http  import HttpResponse, JsonResponse

from products.models import Product, Recipe

class HomeView(View):
    def get(self, request):
        data_caching = Product.objects.prefetch_related('category_set').select_related('season', 'harvest_year', 'measure')
        
        category_deal     = data_caching.filter(is_main=True, discount_rate='', category__name='fresh').values('name', 'category__name', 'big_image2')
        seasonal_deal     = data_caching.filter(is_main=True, season_id__name='september').values('discount_rate', 'name', 'season_id__name', 'big_image1')
        recommand_product = data_caching.all().order_by('id').exclude(is_in_stock=0, big_image1='')[:24].values(
                'id',
                'price',
                'name',
                'small_image',
                'big_image1',
                'big_image2',
                'big_image3',
                'harvest_year_id__year',
                'measure_id__measure',
                'is_on_sale',
                'is_in_stock',
        )
        return JsonResponse({'data' : {'category_deal' : list(category_deal), 'seasonal_deal' : list(seasonal_deal), 'recommand_product' : list(recommand_product)}}, status = 200)
