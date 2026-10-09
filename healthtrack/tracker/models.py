from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    systolic = models.IntegerField(verbose_name="Верхнее давление")
    diastolic = models.IntegerField(verbose_name="Нижнее давление")
    pulse = models.IntegerField(verbose_name="Пульс")
    note = models.TextField(blank=True, verbose_name="Заметка")

    def __str__(self):
        return f"{self.date} - {self.user.username}"