from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Customer(models.Model):
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Customers"

    user = models.OneToOneField(User, null=True, blank=True, related_name='customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def assign_customer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        customer.name = instance.first_name
        customer.surname = instance.last_name
        customer.email = instance.email

        customer.save()


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subCategories', on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "subCategories"

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Sellers"

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Products"

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE, default=1)
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to="static/media", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        items_ordered = self.orderitem_set.all()
        total = 0
        for item in items_ordered:
            total += item.get_total
        return total

    @property
    def get_cart_items(self):
        items_quantity = self.orderitem_set.all()
        total = 0
        for item in items_quantity:
            total += item.quantity
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_time = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Address(models.Model):
    class Meta:
        ordering = ("address",)
        verbose_name_plural = "Address"

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.address
