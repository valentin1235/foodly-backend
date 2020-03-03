import json
import jwt

from .models           import Order, Cart, PackageType, WishList
from products.models   import Product
from account.models    import User
from account.utils     import login_check

from django.views      import View
from django.http       import HttpResponse,JsonResponse
from django.db.models  import F, ExpressionWrapper, DecimalField

class WishListCreateView(View):
    @login_check
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(email=request.user)
            product  = Product.objects.filter(id=data['id'], is_in_stock = True)
            wishlist = WishList.objects.filter(user_id=user, product_id=data['id'])

            if product.exists():
                if wishlist.exists():
                    saved = wishlist.get()
                    saved.quantity = data['quantity']
                    saved.save()
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                WishList.objects.create(product = Product.objects.get(id=data['id']), user=user, quantity=data['quantity'])
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)

        except WishList.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ACTION'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

    @login_check
    def get(self, request):
        saved_list = [
            {
                'name': item.product.name,
                'price': item.product.price,
                'thumbnail_url': item.product.thumbnail_url,
                'quantity': item.quantity
            } for item in WishList.objects.filter(user_id=request.user)
        ]
        return JsonResponse({'wishlist': saved_list}, status=200)

    @login_check
    def delete(self,request):
        data = json.loads(request.body)
        user = User.objects.get(email=request.user)
        wishlist = WishList.objects.filter(user_id=user, product_id=data['id'])

        if wishlist.exists():
            wishlist.get().delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)


class CartView(View):
    @login_check
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = User.objects.get(email = request.user)
            product = Product.objects.filter(id=data['id'], is_in_stock=True)
            cart    = Cart.objects.filter(user_id=user.id, product_id=data['id'])
            order   = Order.objects.filter(user=user, is_closed=False)

            if product.exists():
                if order.exists():
                    if cart.exists():
                        saved_cart = cart.get()
                        saved_cart.quantity = data['quantity']
                        saved_cart.save()
                        return JsonResponse({'message' : 'QTY_CHANGED'}, status=200)
                    Cart.objects.create(
                         user       = user,
                         order      = order.get(),
                         product_id = data['id'],
                         quantity   = data['quantity']
                    )
                    return JsonResponse({'message': 'CART_ADDED'}, status=200)
                Cart.objects.create(
                    user       = user,
                    order      = Order.objects.create(user = user),
                    product_id = data['id'],
                    quantity   = data['quantity']
                )
                return JsonResponse({'message': 'ORDER_CREATED'}, status=200)
            return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

    @login_check
    def delete(self,request):
        data = json.loads(request.body)
        user = User.objects.get(email=request.user)
        cart = Cart.objects.filter(user_id=user, product_id=data['id'])

        if cart.exists():
            cart.get().delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class OrderView(View):
    @login_check
    def get(self,request):
        saved_order = Order.objects.get(user_id=request.user, is_closed=False)
        cart = Order.objects.filter(user_id=request.user, is_closed=False).prefetch_related('cart_set')[0].cart_set.all()

        saved_cart = [
            {
                'name': cart[i].product.name,
                'price': cart[i].product.price,
                'thumbnail_url': cart[i].product.thumbnail_url,
                'quantity': cart[i].quantity
            } for i in range(len(cart))
        ]

        total_q = sum(item['quantity'] for item in saved_cart)
        total_p = Cart.objects.annotate(ttl=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField(10, 2)))

        totals = 0
        i = 0
        while(i < len(total_p)):
            totals += total_p[i].ttl
            i += 1

        sub_total = totals + saved_order.package_type.price
        saved_order.total_price = sub_total
        saved_order.save()

        res = [saved_cart, total_q, saved_order.total_price]
        return JsonResponse({'cart': res}, status=200)