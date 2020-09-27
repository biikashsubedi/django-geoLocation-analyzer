from django import forms
from .models import Measure


class MeasureModelForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ('destination',)
