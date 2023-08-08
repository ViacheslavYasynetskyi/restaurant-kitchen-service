from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, unique=True)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dish"
    )

    class Meta:
        ordering = ["dish_type"]
