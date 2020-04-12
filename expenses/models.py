from django.db import models
from django.conf import settings
# Create your models here.

EXPENSE_STATUSES = (
    ('PENDING', 'PENDING'),
    ('APPROVED', 'APPROVED'),
    ('DECLINED', 'DECLINED')
)


class Expense(models.Model):
    purpose = models.CharField(max_length=255)
    amount = models.FloatField()
    requested_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by_name = models.CharField(max_length=255)
    approval_date = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=255, choices=EXPENSE_STATUSES, default='PENDING')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  max_length=255, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.purpose
