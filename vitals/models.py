from django.db import models
from model_utils.models import TimeStampedModel as TSModel
from django.contrib.auth.models import User

# Create your models here.
class Vital(TSModel):
    WEIGHT = 0
    TEMPERATURE = 1
    SYSTOLIC = 2
    DIASTOLIC = 3
    BPM = 4
    
    VITAL_CHOICES = [
        (WEIGHT, "Weight"),
        (TEMPERATURE, "Temperature"),
        (SYSTOLIC, "Systolic"),
        (DIASTOLIC, "Diastolic"),
        (BPM, "Bpm")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    type = models.IntegerField(choices=VITAL_CHOICES, blank=False, null=False)
    value = models.FloatField(null=False, blank=False)
    