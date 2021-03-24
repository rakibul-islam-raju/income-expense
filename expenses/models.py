from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    description = models.TextField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        User, related_name='expenses', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='expenses', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return self.title
