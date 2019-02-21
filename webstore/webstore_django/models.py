from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=10)
	description = models.TextField()
	cost = models.FloatField()
	def save(self, *args, **kwargs):
		self.cost = round(self.cost, 2)
		super(Product, self).save(*args, **kwargs)

class Shopping_cart(models.Model):
	products = models.TextField(null=True)
	owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
