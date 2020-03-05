import json

from .models           import Order, Cart, PaymentOption, Card, Coupon, PackageType, BillingAddress, WishList
from products.models   import Product
from account.models    import User
from account.utils     import login_check

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import F, ExpressionWrapper, DecimalField

class WishListView(View):
    @login_check
    def post(self, request):
        try:
            data     = json.loads(request.body)
            product  = Product.objects.filter(id=data['id'], is_in_stock = True)
            wishlist = WishList.objects.filter(user_id=request.user, product_id=data['id'])

            if product.exists():
                if wishlist.exists():
                    saved = wishlist.get()
                    saved.quantity = data['quantity']
                    saved.save()
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                WishList.objects.create(product = Product.objects.get(id=data['id']), user=request.user, quantity=data['quantity'])
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
    def delete(self, request):
        data = json.loads(request.body)
        wishlist = WishList.objects.filter(user_id=request.user, product_id=data['id'])

        if wishlist.exists():
            wishlist.get().delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class CartView(View):
    @login_check
    def post(self, request):
        try:
            data    = json.loads(request.body)
            product = Product.objects.filter(id=data['id'], is_in_stock=True)
            cart    = Cart.objects.filter(user_id=request.user, product_id=data['id'])
            order   = Order.objects.filter(user=request.user, is_closed=False)

            if product.exists():
                if order.exists():
                    if cart.exists():
                        saved_cart = cart.get()
                        saved_cart.quantity = data['quantity']
                        saved_cart.save()

                        order.update(package_type=data['package_type_id'])
                        return JsonResponse({'message': 'UPDATED'}, status=200)

                    Cart.objects.create(
                        user=request.user,
                        order=order.get(),
                        product_id=data['id'],
                        quantity=data['quantity']
                    )
                    return JsonResponse({'message': 'NEW_CART_ADDED'}, status=200)
                Cart.objects.create(
                    user=request.user,
                    order=Order.objects.create(user=request.user),

                    product_id=data['id'],
                    quantity=data['quantity']
                )
                return JsonResponse({'message': 'NEW_ORDER_CREATED'}, status=200)
            return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

    @login_check
    def delete(self, request):
        data = json.loads(request.body)
        cart = Cart.objects.filter(user_id=request.user, product_id=data['id'])

        if cart.exists():
            cart.get().delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class OrderView(View):
    @login_check
    def get(self, request):
        saved_order = Order.objects.get(user_id=request.user, is_closed=False)
        cart = saved_order.cart_set.all()

        saved_cart = [
            {
                'name': prop.product.name,
                'price': prop.product.price,
                'thumbnail_url': prop.product.thumbnail_url,
                'quantity': prop.quantity
            } for prop in cart
        ]
        total_q = sum(item['quantity'] for item in saved_cart)
        total_p = Cart.objects.annotate(
            price=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField(10, 2)))

        base = 0
        for each_p in total_p:
            base += each_p.price
        saved_order.total_price = base + saved_order.package_type.price
        saved_order.save()

        shipping_address = Order.objects.get(user_id=request.user).user.address.through.objects.get(user_id=request.user).address
        ship_to = f"{shipping_address.address1}, {shipping_address.city} {shipping_address.state}, {shipping_address.postcode.postcode} {shipping_address.country}"
        shipping_cost = shipping_address.postcode.shipping_cost
        method = f" International Shipping ${shipping_cost}"

        res = [saved_cart, {"total_quantity": total_q}, {"total_price": saved_order.total_price}, {"ship_to": ship_to},{"shipping_cost": method}]
<<<<<<< HEAD
        return JsonResponse({'cart': res}, status=200)

    @login_check
    def post(self,request):
        try:
            data       = json.loads(request.body)
            open_order = Order.objects.filter(user = request.user, is_closed = False)
            coupon     = Coupon.objects.get(discount_code=data['discount_code'])
            payment    = PaymentOption.objects.get(payment=data['payment'])

            BillingAddress(
                user                = request.user,
                is_shipping_address = data['is_shipping_address'],
                first_name          = data['first_name'],
                last_name           = data['last_name'],
                address_1           = data['address_1'],
                address_2           = data['address_2'],
                city                = data['city'],
                country             = data['country'],
                state               = data['state'],
                postcode            = data['postcode']
            ).save()
            billing = BillingAddress.objects.filter(user=request.user).order_by('-id')[0]

            shipping_cost = open_order.get().user.address.through.objects.get(user_id=request.user).address.postcode.shipping_cost

            Order(
                billing_address_id = open_order.update(billing_address_id=billing),
                coupon_id          = open_order.update(coupon_id=coupon),
                payment_option_id  = open_order.update(payment_option_id=payment.id),
                total_price        = open_order.get().total_price  * (1 - coupon.discount_rate if coupon.discount_rate is not None else 0) + shipping_cost
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        except Coupon.DoesNotExist:
            return JsonResponse({"message":"INVALID_COUPONS"}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ACTION'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)