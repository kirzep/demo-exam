from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    article = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    unit = models.CharField(max_length=50, verbose_name='Единица измерения')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    supplier = models.CharField(max_length=255, verbose_name='Поставщик')
    manufacturer = models.CharField(max_length=255, verbose_name='Производитель')
    category = models.CharField(max_length=255, verbose_name='Категория товара')
    discount = models.IntegerField(default=0, verbose_name='Действующая скидка (%)')
    stock = models.IntegerField(default=0, verbose_name='Кол-во на складе')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Фото')

    @property
    def final_price(self):
        if self.discount > 0:
            discount_amount = (self.price * self.discount) / 100
            return round(self.price - discount_amount, 2)
        return self.price

    def __str__(self):
        return f"{self.article} - {self.name}"