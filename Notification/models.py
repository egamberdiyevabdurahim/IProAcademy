from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}/{self.created_at}'
