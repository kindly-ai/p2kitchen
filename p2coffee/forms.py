from django import forms
from p2coffee.models import SensorEvent


class SensorEventForm(forms.ModelForm):
    class Meta:
        model = SensorEvent
        fields = ["name", "value", "id"]
