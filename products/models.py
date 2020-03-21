from django.db import models

class Product(models.Model):
    name            = models.CharField(max_length = 45, unique = True)
    price           = models.DecimalField(max_digits = 10, decimal_places=2, null = True)
    description     = models.CharField(max_length = 1000, null = True)
    small_image     = models.CharField(max_length = 2000, null = True)
    big_image1      = models.CharField(max_length = 2000, null = True)
    big_image2      = models.CharField(max_length = 2000, null = True)
    big_image3      = models.CharField(max_length = 2000, null = True)
    energy          = models.CharField(max_length = 10, null = True)
    carbonydrate    = models.CharField(max_length = 10, null = True)
    protein         = models.CharField(max_length = 10, null = True)
    fat             = models.CharField(max_length = 10, null = True)
    mineral         = models.CharField(max_length = 100, null = True)
    vitamin         = models.CharField(max_length = 100, null = True)
    is_in_stock     = models.CharField(max_length = 30, null = True)
    is_on_sale      = models.BooleanField(default = False)
    discount_rate   = models.CharField(max_length = 50, null = True)
    is_main         = models.BooleanField(default = False)
    harvest_year    = models.ForeignKey('HarvestYear', on_delete = models.SET_NULL, null = True)
    measure         = models.ForeignKey('Measure', on_delete = models.SET_NULL, null = True)
    recipe          = models.ForeignKey('Recipe', on_delete = models.SET_NULL, null = True)
    season          = models.ForeignKey('Season', on_delete = models.SET_NULL, null = True)
    similar_product = models.ManyToManyField('self', through = 'SimilarProduct', symmetrical = False)
    bundle          = models.ManyToManyField('Bundle', through = 'ProductBundle')
    category        = models.ManyToManyField('Category', through = 'ProductCategory')
    
    class Meta:
        db_table = 'products'

class HarvestYear(models.Model):
    year = models.CharField(max_length = 45)
    
    class Meta:
        db_table = 'harvest_years'

class Measure(models.Model):
    measure = models.CharField(max_length = 10)
    
    class Meta:
        db_table = 'measures'

class Season(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'seasons'

class SimilarProduct(models.Model):
    from_product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name = 'from_product')
    to_product   = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True, related_name = 'to_product')
    
    class Meta:
        unique_together = ('from_product', 'to_product')
        db_table        = 'similar_products'

class Bundle(models.Model):
    title           = models.CharField(max_length = 100)
    price           = models.CharField(max_length = 50, null = True)
    is_in_promotion = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'bundles'

class ProductBundle(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE, null = True)
    bundle  = models.ForeignKey('Bundle', on_delete = models.CASCADE, null = True)
    
    class Meta:
        db_table = 'product_bundles'

class Category(models.Model):
    name        = models.CharField(max_length = 50, null = True)
    image_url   = models.CharField(max_length = 2000, null = True)
    description = models.CharField(max_length = 2000, null = True)

    class Meta:
        db_table = 'categories'
    
class ProductCategory(models.Model):
    product  = models.ForeignKey('Product', on_delete = models.CASCADE, null = True)
    category = models.ForeignKey('Category', on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'product_categories'

class Recipe(models.Model):
    title          = models.CharField(max_length = 100, null = True)
    ingredient     = models.CharField(max_length = 2000, null = True)
    thumbnail_url  = models.CharField(max_length = 2000, null = True)
    company        = models.CharField(max_length = 45, null = True)
    posting_date   = models.CharField(max_length = 45, null = True)
    author         = models.CharField(max_length = 100, null = True)
    direction      = models.TextField(null = True)
    description    = models.TextField(null = True)
    is_main        = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'recipes'

class Keyword(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    
    class Meta:
        db_table = 'keywords'

class RecipeKeyword(models.Model):
    recipe    = models.ForeignKey('Recipe', on_delete = models.CASCADE, null = True)
    keyword   = models.ForeignKey('Keyword', on_delete = models.CASCADE, null = True)
    
    class Meta:
        db_table = 'recipe_keywords'

class Recommendation(models.Model):
    title         = models.CharField(max_length = 100)
    description   = models.CharField(max_length = 1000)
    recipe        = models.ManyToManyField('Recipe', through = 'RecipeRecommendation')
    is_on_display = models.BooleanField(default = True)

    class Meta:
        db_table = 'recommendations'

class RecipeRecommendation(models.Model):
    recipe         = models.ForeignKey('Recipe', on_delete = models.CASCADE, null = True)
    recommendation = models.ForeignKey('Recommendation', on_delete = models.CASCADE, null = True)
    
    class Meta:
        db_table = 'recipe_recommendations'


