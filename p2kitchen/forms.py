from django import forms

from p2kitchen.models import SensorEvent


class SensorEventForm(forms.ModelForm):
    class Meta:
        model = SensorEvent
        fields = ["name", "value", "id", "device_name"]
