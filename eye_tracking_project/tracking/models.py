
from django.db import models

class Participant(models.Model):
    participant_id = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

class EyeTrackingData(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    csv_file = models.FileField(upload_to='csv/', null=True, blank=True)
    processed = models.BooleanField(default=False)

