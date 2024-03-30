from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class User(AbstractUser):
    STATUS = (
        ('Admin', 'Admin'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('User', 'User'),
    )

    phone = models.CharField(max_length=14, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photo/', default='base.jpg')
    status = models.CharField(max_length=12, choices=STATUS, default='Student')

    def __str__(self):
        return f'{self.first_name}/{self.status}'
