from django.db import models

# Create your models here.

EXPENSE_STATUSES = (
    ('PENDING', 'PENDING'),
    ('DISBURSED', 'DISBURSED')
)


class Expense(models.Model):
    purpose = models.CharField(max_length=255)
    amount = models.FloatField()
    requested_on = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=255, choices=EXPENSE_STATUSES, default='PENDING')
    requester = models.CharField(max_length=255)

    def __str__(self):
        return self.purpose
