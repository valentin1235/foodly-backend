from django.db import models


# Create your models here.

class Account(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="이름")
    last_name = models.CharField(max_length=200, verbose_name="성")
    email = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'accounts'
