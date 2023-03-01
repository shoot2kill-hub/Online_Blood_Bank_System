from django import forms

from . import models


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['hospital_name','address','mobile','reason','bloodgroup','unit']
