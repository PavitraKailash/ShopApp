from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customers(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    cst_phone = models.IntegerField()
    is_seller = models.BooleanField(default=False)


class ProductDetails(models.Model):
    pdt_id = models.AutoField(primary_key=True)
    pdt_name = models.CharField(max_length=70)
    pdt_descp = models.CharField(max_length=70)
    stk_no = models.IntegerField(null=True, blank=True)
    pdt_price = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True, null=True)
    stk_upto = models.DateTimeField(null=True)
    is_empty = models.BooleanField(null=True)


class Cart(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_checkout = models.BooleanField(null=True, default=False)


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        ProductDetails,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.product.title, self.quantity)


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        related_name='orders',
            on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cart = models.ForeignKey(
        Cart,
        related_name='orders',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    total_products = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


