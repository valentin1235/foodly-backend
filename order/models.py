from account.models import User
from products.models import Product

from django.db import models

class Order(models.Model):
    user            = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    payment_option  = models.ForeignKey("PaymentOption", on_delete = models.SET_NULL, null = True)
    coupon          = models.ForeignKey("Coupon", on_delete = models.SET_NULL, null = True)
    billing_address = models.ForeignKey("BillingAddress", on_delete = models.SET_NULL, null = True)
    created_at      = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    user         = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    order        = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    product      = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    package_type = models.ForeignKey("PackageType", on_delete = models.SET_NULL, null = True)
    quantity     = models.IntegerField()

    class Meta:
        db_table = 'carts'

class BillingAddress(models.Model):
    postcode            = models.IntegerField()
    is_shipping_address = models.BooleanField(default = True)
    first_name          = models.CharField(max_length = 45)
    last_name           = models.CharField(max_length = 45)
    address_1           = models.CharField(max_length = 200)
    address_2           = models.CharField(max_length = 200)
    city                = models.CharField(max_length = 200)
    state               = models.CharField(max_length = 200)
    country             = models.CharField(max_length = 200)

    class Meta:
        db_table = 'billing_addresses'

class PaymentOption(models.Model):
    type = models.CharField(max_length = 100)

    class Meta:
        db_table = 'payment_options'

class Card(models.Model):
    payment_option   = models.ForeignKey(PaymentOption, on_delete = models.SET_NULL, null = True)
    card_number      = models.IntegerField()
    card_type        = models.CharField(max_length = 45)
    card_holder      = models.CharField(max_length = 100)
    bank             = models.CharField(max_length = 100)
    expiration_year  = models.CharField(max_length = 10)
    expiration_month = models.CharField(max_length = 10)
    cvv              = models.IntegerField()

    class Meta:
        db_table = 'cards'

class Coupon(models.Model):
    discount_code = models.CharField(max_length = 45)
    discount_rate = models.DecimalField(max_digits = 3, decimal_places = 2)

    class Meta:
        db_table = 'coupons'

class PackageType(models.Model):
    type  = models.CharField(max_length = 45)
    price = models.DecimalField(max_digits = 3, decimal_places = 2)

    class Meta:
        db_table = 'package_types'

class WishList(models.Model):
    product  = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    user     = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'wishlists'

