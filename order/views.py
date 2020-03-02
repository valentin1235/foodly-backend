import json

from .models        import Order, Cart, PaymentOption, Card, Coupon, PackageType, BillingAddress, WishList
from products.models import Product
from user.models    import User

from django.views import View
from django.http  import HttpResponse,JsonResponse


class WishListCreateView(View):
#    @token_check_decorator
    def post(self, request):

        try:
            wishlist_data = json.loads(request.body)
            wishlist_user = User.objects.get(email = wishlist_data['email'])        # token_check_decorator가 완성되면, (email = request.user)
            new_item      = Product.objects.get(name = wishlist_data['product'])

            if Product.objects.filter(name = wishlist_data['product'], is_in_stock = True).exists():
                WishList.objects.create(product = new_item, user = wishlist_user, quantity = wishlist_data['quantity'])
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            else:
                return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)

        except WishList.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ACTION'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

#   @token_check_decorator
    def get(self, request):
        signed_in_user = User.objects.get(id = 1)    # token_check_decorator가 완성되면 삭제할 코드
        saved_wishlist = WishList.objects.filter(user_id = signed_in_user)  # token_check_decorator가 완성되면, (user_id = request.user)

        saved_list = [
            {
                'name': item.product.name,
                'price': item.product.price,
                'thumbnail_url': item.product.thumbnail_url,
                'quantity': item.quantity
            } for item in saved_wishlist]

        return JsonResponse({'wishlist': saved_list}, status=200)

#   @token_check_decorator
    def delete(self,request):
        data = json.loads(request.body)

        if WishList.objects.filter(id=data['id']).exists():
            WishList.objects.get(id=data['id']).delete()
            return JsonResponse({"message": "SUCCESS"}, status=200)
        return JsonResponse({"message": "INVALID_INPUT"}, status=200)

class CartView(View):
#    @token_check_decorator
    def post(self, request):
        try:
            order_data   = json.loads(request.body)
            order_user   = User.objects.get(email = order_data['email']) # token_check_decorator가 완성되면, (email = request.user)
            product      = Product.objects.filter(id=order_data['id'], is_in_stock=True)
            cart         = Cart.objects.filter(user_id = order_user.id, product_id = order_data['id'])
            order        = Order.objects.filter(user = order_user)

            if product.exists():
                if order.exists():
                    if cart.exists():
                        cart_to_update = cart.get(product_id=order_data["id"])
                        cart_to_update.quantity = int(order_data['quantity']) + cart_to_update.quantity
                        cart_to_update.save()
                        return JsonResponse({'message' : 'CART_ADDED'}, status=200)
                    
                    Cart.objects.create(
                        user       = order_user,
                        order      = order.get(user=order_user),
                        product_id = order_data['id'],
                        quantity   = order_data['quantity']
                    )
                    return JsonResponse({'message': 'CART_CREATED'}, status=200)
               
                new_order = Order.objects.create(user = order_user)
                Cart.objects.create(
                    user = order_user,
                    order = new_order,
                    product_id = order_data['id'],
                    quantity = order_data['quantity']
                )
                return JsonResponse({'message': 'ORDER_CREATED'}, status=200)
            
            return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
