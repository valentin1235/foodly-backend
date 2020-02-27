from django.db import models

# Create your models here.
class Product(models.Model):
    name          = models.CharField(max_length = 45, unique = True)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    description   = models.CharField(max_length=1000)
    is_in_stock   = models.BooleanField(default = True)
    thumbnail_url = models.CharField(max_length = 2000)
    is_on_sale    = models.BooleanField(default = False)
    energy        = models.CharField(max_length = 10)
    carbonydrate  = models.CharField(max_length = 10)
    protein       = models.CharField(max_length = 10)
    total_fat     = models.CharField(max_length = 10)
    dietary_fiber = models.CharField(max_length = 10)
    harvest_year  = models.ForeignKey('HarvestYear', on_delete = models.SET_NULL, null=True)
    measure       = models.ForeignKey('Measure', on_delete = models.SET_NULL, null=True)
    color         = models.ForeignKey('Color', on_delete = models.SET_NULL, null=True)
    wood_type     = models.ForeignKey('WoodType', on_delete = models.SET_NULL, null=True)
    recipe        = models.ForeignKey('Recipe', on_delete = models.SET_NULL, null=True)
    similar_product = models.ManyToManyField('self', through = 'SimilarProduct', symmetrical = False)
    mineral       = models.ManyToManyField('Mineral', through = 'ProductMineral')
    vitamin       = models.ManyToManyField('Vitamin', through = 'ProductVitamin')
    bundle        = models.ManyToManyField('Bundle', through = 'ProductBundle')

    class Meta:
        db_table = 'products'

class HarvestYear(models.Model):
    year = models.CharField(max_length = 45, unique = True)
    class Meta:
        db_table = 'harvest_years'

class Measure(models.Model):
    measure = models.CharField(max_length = 10, unique = True)
    class Meta:
        db_table = 'measures'

class Color(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    class Meta:
        db_table = 'colors'

class WoodType(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    class Meta:
        db_table = 'wood_types'

class SimilarProduct(models.Model):
    from_product = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True, related_name = 'from_product')
    to_product   = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True, related_name = 'to_product')
    class Meta:
        unique_together = ('from_product', 'to_product')
        db_table = 'similar_products'

class Mineral(models.Model):
    name = models.CharField(max_length = 10, unique = True)
    class Meta:
        db_table = 'minerals'

class ProductMineral(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, null=True)
    mineral = models.ForeignKey('Mineral', on_delete = models.CASCADE, null=True)
    class Meta:
        db_table = 'product_minerals'

class Vitamin(models.Model):
    name = models.CharField(max_length = 10, unique = True)
    class Meta:
        db_table = 'vitamins'

class ProductVitamin(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, null=True)
    vitamin = models.ForeignKey('Vitamin', on_delete = models.CASCADE, null=True)
    class Meta:
        db_table = 'product_vitamins'

class Bundle(models.Model):
    title = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    is_main = models.BooleanField(default = False)
    class Meta:
        db_table = 'bundles'

class ProductBundle(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, null=True)
    bundle = models.ForeignKey('Bundle', on_delete = models.CASCADE, null=True)
    class Meta:
        db_table = 'product_bundles'

#class Review(models.Model):
#    user       = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
#    product    = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
#    review     = models.TextField()
#    created_at = models.DateTimeField(auto_now_add = True)
#    updated_at = models.DateTimeField(auto_now = True)
#    class Meta:
#        db_table = 'reviews'



class Recipe(models.Model):
    title          = models.CharField(max_length = 100)
    ingredient     = models.CharField(max_length = 2000)
    direction      = models.TextField()
    thumbnail_url  = models.CharField(max_length = 2000)
    company        = models.CharField(max_length = 45)
    class Meta:
        db_table = 'recipes'

class Filtering(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    class Meta:
        db_table = 'filterings'

class RecipeFiltering(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete = models.CASCADE, null = True)
    filtering = models.ForeignKey('Filtering', on_delete = models.CASCADE, null = True)
    class Meta:
        db_table = 'recipe_filterings'

class Recommendation(models.Model):
    title       = models.CharField(max_length = 100)
    description = models.CharField(max_length = 1000)
    class Meta:
        db_table = 'recommendations'

class RecipeRecommendation(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete = models.CASCADE, null=True)
    recommendation = models.ForeignKey('Recommendation', on_delete = models.CASCADE, null=True)
    class Meta:
        db_table = 'recipe_recommendations'


