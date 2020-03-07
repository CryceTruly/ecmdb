from django.db import models

# Create your models here.


class Bank(models.Model):
    name = models.CharField(max_length=255, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
