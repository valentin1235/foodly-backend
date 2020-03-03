import  json

from django.db    import IntegrityError
from django.views import View
from django.http  import HttpResponse, JsonResponse

from products.models import Product, Recipe

class HomeView(View):
    def get(self, request):
        caching_field = Product.objects.select_related('harvest_year', 'measure')
        product_info  = caching_field.all().order_by('id').exclude(is_in_stock=0)[:24].values(
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
        )
        return JsonResponse({'data' : list(product_info)}, status = 200)
