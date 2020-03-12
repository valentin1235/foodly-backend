from django.db       import models
from account.models  import User
from products.models import Product


# Create your models here.

class Review(models.Model):
    user      = models.ForeignKey('account.User', on_delete=models.CASCADE)
    review    = models.TextField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product   = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'
