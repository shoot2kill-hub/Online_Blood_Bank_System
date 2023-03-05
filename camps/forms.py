from django import forms
from camps.models import Hospital_service
from donor.models import LabResult


class HospitalServiceForm(forms.ModelForm):
    class Meta:
        model = Hospital_service
        fields = ['hospital_name', 'hospital_location', 'hospital_start_time', 'hospital_date_donating',
                  'hospital_end_time', 'hospital_phone']


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['hepatitis', 'cancer', 'hiv', 'diabetes', 'malaria', 'approve_blood']
