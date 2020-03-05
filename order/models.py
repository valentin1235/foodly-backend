import uuid

from account.models import User
from products.models import Product

from django.db import models

class PaymentOption(models.Model):
    payment = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = 'payment_options'

class Card(models.Model):
    payment_option   = models.ForeignKey(PaymentOption, on_delete = models.SET_NULL, null = True)
    card_number      = models.CharField(max_length = 100, unique = True)
    card_holder      = models.CharField(max_length = 100)
    expiration_year  = models.CharField(max_length = 10)
    expiration_month = models.CharField(max_length = 10)
    cvv              = models.CharField(max_length = 100)

    class Meta:
        db_table = 'cards'

class Coupon(models.Model):
    discount_code = models.CharField(max_length = 45, null = True, unique = True)
    discount_rate = models.DecimalField(max_digits = 3, decimal_places = 2, null = True)
    is_used       = models.BooleanField(default=False)

    class Meta:
        db_table = 'coupons'

class BillingAddress(models.Model):
    user                = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    postcode            = models.IntegerField(null = True)
    is_shipping_address = models.BooleanField(default = True)
    first_name          = models.CharField(max_length = 45, null = True)
    last_name           = models.CharField(max_length = 45, null = True)
    address_1           = models.CharField(max_length = 200, null = True)
    address_2           = models.CharField(max_length = 200, null = True)
    city                = models.CharField(max_length = 200, null = True)
    state               = models.CharField(max_length = 200, null = True)
    country             = models.CharField(max_length = 200, null = True)

    class Meta:
        db_table = 'billing_addresses'

class PackageType(models.Model):
    package  = models.CharField(max_length = 45, unique = True)
    price    = models.DecimalField(max_digits = 3, decimal_places = 2)

    class Meta:
        db_table = 'package_types'

def get_pt():
    return PackageType.objects.get(id=1).id

class Order(models.Model):
    id               = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    user             = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    package_type     = models.ForeignKey(PackageType,default=get_pt, on_delete = models.CASCADE)
    payment_option   = models.ForeignKey(PaymentOption,on_delete = models.CASCADE, null = True)
    coupon           = models.ForeignKey(Coupon, on_delete = models.SET_NULL, null = True)
    billing_address  = models.ForeignKey(BillingAddress, on_delete = models.SET_NULL, null = True)
    created_at       = models.DateTimeField(auto_now_add = True)
    total_price      = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    is_closed        = models.BooleanField(default = False)

    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    user         = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    order        = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    product      = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    quantity     = models.IntegerField()

    class Meta:
        db_table = 'carts'


class WishList(models.Model):
    product  = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    user     = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'wishlists'

