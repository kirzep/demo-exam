from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Авторизованный клиент'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name='Роль')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip() or self.username