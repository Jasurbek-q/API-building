from django.db import models
from django.contrib.auth.models import User


class Vacancy(models.Model):
    #vakanisyani kim yaratganini bilish uchun User modeliga boglaymiz(Foreign key)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Elon muallifi')
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.CharField(max_length=100, verbose_name='Company')
    salary = models.PositiveIntegerField(null=True, blank=True, verbose_name='Maosh')
    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.company}"

