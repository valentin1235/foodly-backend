import jwt, bcrypt, json

from django.db    import IntegrityError
from django.views import View
from django.http  import HttpResponse, JsonResponse

from foodly_project.my_settings import SECRET_KEY
from .models import Product
#from .utils  import login_required

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


