from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from products.models import Product

class PickupPoint(models.Model):
    address = models.CharField(max_length=255, verbose_name='Адрес пункта выдачи')

    def __str__(self):
        return self.address

class Order(models.Model):
    STATUS_CHOICES = [
        ('Новый', 'Новый'),
        ('Завершен', 'Завершен'),
    ]
    
    order_number = models.IntegerField(unique=True, verbose_name='Номер заказа')
    date_created = models.DateField(verbose_name='Дата заказа')
    date_delivery = models.DateField(verbose_name='Дата доставки')
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, verbose_name='Пункт выдачи')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    receive_code = models.IntegerField(verbose_name='Код для получения')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Новый', verbose_name='Статус заказа')

    def __str__(self):
        return f"Заказ №{self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT) 
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} х {self.quantity}"