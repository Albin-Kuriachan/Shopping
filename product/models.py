from django.db import models
from account.models import CustomUser


class Category(models.Model):
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category_image", null=True, blank=True)

    def __str__(self):
        return self.category


class ProductDetails(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ManyToManyField(Category, blank=True)
    display = models.BooleanField(default=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="product_image", null=True, blank=True)
    total_quantity = models.PositiveIntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return self.product_name




class Quantity(models.Model):
    DENOMINATION = [
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        ('l', 'l'),
    ]
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE, blank=True, null=True)
    no_quantity = models.PositiveIntegerField(null=True, blank=True)
    weight_litter = models.PositiveIntegerField(null=True, blank=True)
    denominations = models.CharField(max_length=10, choices=DENOMINATION, default=None)
    price = models.PositiveIntegerField(null=True, blank=True)
    old_price = models.PositiveIntegerField(null=True, blank=True)



    def __str__(self):
        return f"{self.product.product_name} - {self.weight_litter}{self.denominations}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.total_quantity = self.product.quantity_set.aggregate(total=models.Sum('no_quantity'))['total'] or 0
        self.product.save()

