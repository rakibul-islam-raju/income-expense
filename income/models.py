from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name='sources', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Income(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    description = models.TextField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        User, related_name='incomes', on_delete=models.CASCADE)
    source = models.ForeignKey(
        Source, related_name='incomes', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return self.title
