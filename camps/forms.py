from django import forms
from camps.models import Hospital_service


class HospitalServiceForm(forms.ModelForm):
    class Meta:
        model = Hospital_service
        fields = ['camp_name', 'camp_location', 'camp_start_time', 'camp_end_time', 'camp_phone']