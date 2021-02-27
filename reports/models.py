from django.db import models
from django.conf import settings


# iterable
PURPOSE_CHOICES = (
    ("MORTGAGE", "MORTGAGE"),
    ("EXPROPRIATION", "EXPROPRIATION"),
    ("EVALUATION", "EVALUATION"),
    ("LAND SUBDIVISION", "LAND SUBDIVISION"),
    ("CONSTRUCTION STAKEOUTS", "CONSTRUCTION STAKEOUTS"),
    ("ZONING PLATS", "ZONING PLATS"),
    ("VOLUME ANALYSIS SURVEY", "VOLUME ANALYSIS SURVEY"),
    ("TOPOGRAPHIC SURVEYS", "TOPOGRAPHIC SURVEYS"),
    ("FLOODING ANALYSIS", "FLOODING ANALYSIS"),
    ("LOT GRADING PLANS", "LOT GRADING PLANS"),
    ("HYDRO GRAPHIC SURVEY", "HYDRO GRAPHIC SURVEY"),
)


class Report(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   max_length=255, on_delete=models.CASCADE)
    owner = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    amount = models.FloatField(max_length=255, blank=True)
    client = models.CharField(max_length=255)
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES)
    inspection_date = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    upi = models.CharField(
        null=False, blank=False, unique=True, max_length=255)
    report_payed_for = models.BooleanField(default=False)
    reason_for_not_paying = models.TextField()
    delivery_date = models.CharField(max_length=255)
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True)

    report_file = models.FileField(upload_to='documents')
    paid = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True)
    approved_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.purpose + ' in ' + self.location


class Comment(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   max_length=255, on_delete=models.CASCADE)
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.message
