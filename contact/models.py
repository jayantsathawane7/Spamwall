from django.contrib.auth.models import User
from django.db import models

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, primary_key=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class SpamReport(models.Model):
    phone_number = models.CharField(max_length=15, primary_key=True)
    spam_count = models.PositiveIntegerField(default=0)
    reported_by = models.ManyToManyField(User, related_name='reported_spam', blank=True)

    def __str__(self):
        return f"{self.phone_number} ({self.spam_count} reports)"

