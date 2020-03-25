import json

from .models           import Order, Cart, PaymentOption, Card, Coupon, BillingAddress, WishList
from products.models   import Product
from account.models    import User
from account.utils     import login_check

from django.views      import View
from django.http       import HttpResponse, JsonResponse
from django.db.models  import F, ExpressionWrapper, DecimalField

class WishListView(View):
    @login_check
    def post(self, request):
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=data['id'])
            wishlist = WishList.objects.filter(user=request.user, product_id=data['id'])

            if wishlist.exists():
                wishlist.update(quantity=data['quantity'])

                return HttpResponse(status=200)

            WishList.objects.create(product=product,
                                    user=request.user,
                                    quantity=data['quantity'])

            return HttpResponse(status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRDUCT_ID'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

    @login_check
    def get(self, request):
        saved_list = [
            {
                'name'          : item.product.name,
                'price'         : item.product.price,
                'small_image'   : item.product.small_image,
                'quantity'      : item.quantity
            } for item in WishList.objects.filter(user=request.user)
        ]
        return JsonResponse({'wishlist': saved_list}, status=200)

    @login_check
    def delete(self, request):
        data = json.loads(request.body)
        wishlist = WishList.objects.filter(user=request.user, product_id=data['id'])

        if wishlist.exists():
            wishlist.get().delete()

            return HttpResponse(status=200)

        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class CartView(View):
    @login_check
    def post(self, request):
        try:
            data    = json.loads(request.body)
            product = Product.objects.filter(id=data['id'], is_in_stock=True)

            if not product.exists():
                return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)
 
            cart    = Cart.objects.filter(user=request.user, product_id=data['id'])
            order   = Order.objects.filter(user=request.user, is_closed=False)

            if order.exists():
                if cart.exists():
                    cart.update(quantity=data['quantity'])
                    order.update(package_type_id=data['package_type_id'])

                    return HttpResponse(status=200)

                Cart.objects.create(
                    user        = request.user,
                    order       = order.get(),
                    product_id  = data['id'],
                    quantity    = data['quantity']
                )
                return HttpResponse(status=200)

            else:
                Cart.objects.create(
                    user        = request.user,
                    order       = Order.objects.create(user=request.user),
                    product_id  = data['id'],
                    quantity    = data['quantity']
                )
                return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

    @login_check
    def delete(self, request):
        data = json.loads(request.body)
        cart = Cart.objects.filter(user=request.user, product_id=data['id'])

        if cart.exists():
            cart.get().delete()

            return HttpResponse(status=200)

        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class OrderView(View):
    @login_check
    def get(self, request):
        try:
            saved_order = Order.objects.get(user=request.user, is_closed=False)
            cart        = saved_order.cart_set.all()

            saved_cart = [
                {
                    'name'          : prop.product.name,
                    'price'         : prop.product.price,
                    'small_image'   : prop.product.small_image,
                    'quantity'      : prop.quantity
                } for prop in cart
            ]

            total_quantity  = sum(item['quantity'] for item in saved_cart)
            total_price     = Cart.objects.annotate(price=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField(10, 2)))

            base = 0
            for each_price in total_price:
                base += each_price.price
            saved_order.total_price = base + saved_order.package_type.price
            saved_order.save()

            shipping_address = request.user.user_address_set.get(address_id__is_default=True)

            res = [saved_cart,
                {"total_quantity"   : total_quantity},
                {"total_price"      : saved_order.total_price},
                {"address1"         : shipping_address.address.address1},
                {"address2"         : shipping_address.address.address2},
                {"city"             : shipping_address.address.city},
                {"state"            : shipping_address.address.state},
                {"postcode"         : shipping_address.address.postcode.postcode},
                {"country"          : shipping_address.address.country},
                {"shipping_cost"    : shipping_address.address.postcode.shipping_cost}
            ]
            return JsonResponse({'cart': res}, status=200)

        except Order.DoesNotExist():
            return JsonResponse({"message":"NO_ORDERS"}, status=400)

        except Cart.DoesNotExist():
            return JsonResponse({"message":"NO_CARTS"}, status=400)        

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

            shipping_cost = request.user.user_address_set.get(address_id__is_default=True).address.postcode.shipping_cost

            Order(
                billing_address_id = open_order.update(billing_address_id=billing),
                coupon_id          = open_order.update(coupon_id=coupon),
                payment_option_id  = open_order.update(payment_option_id=payment.id),
                total_price        = open_order.get().total_price  * (1 - coupon.discount_rate if coupon.discount_rate is not None else 0) + shipping_cost
            ).save()

            coupon.is_used= True

            return HttpResponse(status=200)

        except Coupon.DoesNotExist:
            return JsonResponse({"message":"INVALID_COUPONS"}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ACTION'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

class ReceiptView(View):
    @login_check
    def get(self, request):
        saved_order = Order.objects.get(user=request.user, is_closed=False)
        cart = saved_order.cart_set.all()

        saved_cart = [
            {
                'name': prop.product.name,
                'price': prop.product.price,
                'quantity': prop.quantity
            } for prop in cart
        ]

        shipping_address = request.user.user_address_set.get(address_id__is_default=True)

        saved_order.is_closed = True
        saved_order.save()

        res = [saved_order.user.first_name,
               saved_order.user.last_name,saved_order.payment_option.payment,
               shipping_address.address.address1,
               shipping_address.address.address2,
               shipping_address.address.city,
               shipping_address.address.state,
               shipping_address.address.postcode.postcode,
               shipping_address.address.country,
               saved_cart,
               saved_order.total_price,
               saved_order.package_type.package
        ]

        return JsonResponse({'receipt': res}, status=200)
