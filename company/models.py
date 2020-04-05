from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(("email"), max_length=254)
    phone_number = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "About Company"

    def __str__(self):
        return self.name
