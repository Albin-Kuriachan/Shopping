from django.db import models
from account.models import CustomUser
from product.models import ProductDetails, Quantity



class User_Data(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Cart(models.Model):
    STAGE = [
        ('Cart', 'Cart'),
        ('Order', 'Order'),
    ]

    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_data = models.ForeignKey(User_Data, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(ProductDetails, on_delete=models.SET_NULL,null=True, blank=True)
    quantity = models.ForeignKey(Quantity, on_delete=models.SET_NULL,null=True, blank=True)
    product_name = models.CharField(max_length=30, null=True, blank=True)
    product_quantity = models.CharField(max_length=30, null=True, blank=True)
    selected_no = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    stage = models.CharField(max_length=10, choices=STAGE, default='Cart')
    address = models.TextField(max_length=200, blank=True, null=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Pending')

    def __str__(self):
        return self.product_name


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


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number=models.IntegerField(null=True, blank=True)
    month=models.CharField(max_length=10,null=True, blank=True)
    year=models.IntegerField(null=True, blank=True)


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    my_review=models.TextField(max_length=100,null=True, blank=True)


