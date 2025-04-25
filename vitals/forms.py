from django import forms
from .models import Vital
from datetime import datetime

class BloodForm(forms.Form):
    date = forms.DateTimeField(required=True, initial=datetime.now)
    systolic = forms.FloatField(required=True)
    diastolic = forms.FloatField(required=True)
    bpm = forms.FloatField(required=True)

    def save(self, user):
        if self.is_valid():
            data = self.cleaned_data

            date = data['date']
            
            sys = Vital()

            sys.date = date
            sys.user = user
            sys.type = Vital.SYSTOLIC
            sys.value = data['systolic']
            sys.save()

            dia = Vital()

            dia.date = date
            dia.user = user
            dia.type = Vital.DIASTOLIC
            dia.value = data['diastolic']
            dia.save()

            bpm = Vital()
            bpm.date = date
            bpm.user = user
            bpm.type = Vital.BPM
            bpm.value = data['bpm']
            bpm.save()
