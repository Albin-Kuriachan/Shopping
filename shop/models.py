from django.db import models
from account.models import CustomUser
from product.models import ProductDetails, Quantity


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
    selected_no = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    phone2 = models.PositiveIntegerField(null=True, blank=True)
    address_line = models.CharField(max_length=200, null=True, blank=True)
    house_no = models.PositiveIntegerField(null=True, blank=True)
    pin_code = models.PositiveIntegerField(null=True, blank=True)
    place = models.CharField(max_length=30, null=True, blank=True)
    landmark = models.CharField(max_length=30, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If this address is set as default, ensure others are not
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super(Address, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cart_data = models.ManyToManyField(Cart)
    created_at = models.DateTimeField(auto_now_add=True)
    amount_payed = models.IntegerField(null=True, blank=True)

    # def total_price(self):
    #     total = 0
    #     for item in self.cart_data.all():
    #         total += item.price
    #     return total
    #
    #
    #
    # def __str__(self):
    #     return f"Order {self.id} - User: {self.user.username}, Total: {self.total_price()}"
