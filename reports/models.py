from django.db import models
from django.conf import settings
# Create your models here.


# iterable
PURPOSE_CHOICES = (
    ("MORTGAGE", "MORTGAGE"),
    ("EXPROPRIATION", "EXPROPRIATION"),
    ("EVALUATION", "EVALUATION"),
)


class Report(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              max_length=255, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    amount_charged = models.FloatField()
    client = models.CharField(max_length=255)
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES)
    inspection_date = models.DateField()
    report_payed_for = models.BooleanField(default=False)
    reason_for_not_paying = models.TextField()
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
