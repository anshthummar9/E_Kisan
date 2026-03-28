from django.db import models
from django.contrib.auth.models import User

class SoilReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    soil_color = models.CharField(max_length=50) # e.g., Black, Red
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    temperature = models.FloatField()
    predicted_crop = models.CharField(max_length=100)
    predicted_fertilizer = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_crop} ({self.created_at.strftime('%Y-%m-%d')})"
