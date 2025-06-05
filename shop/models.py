from django.db import models
from django.contrib.auth.models import User

class  Category(models.Model):
	name = models.CharField(max_length = 100)
	def __str__(self):
		return self.name
class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	available = models.BooleanField(default=True)
	image = models.ImageField(upload_to='product_images/', blank=True, null=True)
	
	def __str__(self):
		return self.name
		
class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	is_delivered = models.BooleanField(default=False)
	
	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"

