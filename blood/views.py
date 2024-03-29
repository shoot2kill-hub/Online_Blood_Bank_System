from django.shortcuts import render, redirect, reverse, HttpResponse

from donor.models import LabResult
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from donor import models as dmodels
from patient import models as pmodels
from donor import forms as dforms
from patient import forms as pforms
from camps.forms import HospitalServiceForm
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
import datetime
import tempfile
from blood.utilis import send_sms
from camps.forms import LabResultForm


def home_view(request):
    x = models.Stock.objects.all()
    print(x)
    if len(x) == 0:
        blood1 = models.Stock()
        blood1.bloodgroup = "A+"
        blood1.save()

        blood2 = models.Stock()
        blood2.bloodgroup = "A-"
        blood2.save()

        blood3 = models.Stock()
        blood3.bloodgroup = "B+"
        blood3.save()

        blood4 = models.Stock()
        blood4.bloodgroup = "B-"
        blood4.save()

        blood5 = models.Stock()
        blood5.bloodgroup = "AB+"
        blood5.save()

        blood6 = models.Stock()
        blood6.bloodgroup = "AB-"
        blood6.save()

        blood7 = models.Stock()
        blood7.bloodgroup = "O+"
        blood7.save()

        blood8 = models.Stock()
        blood8.bloodgroup = "O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'blood/index.html')


def is_donor(user):
    return user.groups.filter(name='DONOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def afterlogin_view(request):
    if is_donor(request.user):
        return redirect('donor/donor-dashboard')

    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        return redirect('admin-dashboard')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit = models.Stock.objects.aggregate(Sum('unit'))
    dict = {

        'A1': models.Stock.objects.get(bloodgroup="A+"),
        'A2': models.Stock.objects.get(bloodgroup="A-"),
        'B1': models.Stock.objects.get(bloodgroup="B+"),
        'B2': models.Stock.objects.get(bloodgroup="B-"),
        'AB1': models.Stock.objects.get(bloodgroup="AB+"),
        'AB2': models.Stock.objects.get(bloodgroup="AB-"),
        'O1': models.Stock.objects.get(bloodgroup="O+"),
        'O2': models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors': dmodels.Donor.objects.all().count(),
        'totalbloodunit': totalunit['unit__sum'],
        'totalrequest': models.BloodRequest.objects.all().count(),
        'totalapprovedrequest': models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request, 'blood/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict = {
        'bloodForm': forms.BloodForm(),
        'A1': models.Stock.objects.get(bloodgroup="A+"),
        'A2': models.Stock.objects.get(bloodgroup="A-"),
        'B1': models.Stock.objects.get(bloodgroup="B+"),
        'B2': models.Stock.objects.get(bloodgroup="B-"),
        'AB1': models.Stock.objects.get(bloodgroup="AB+"),
        'AB2': models.Stock.objects.get(bloodgroup="AB-"),
        'O1': models.Stock.objects.get(bloodgroup="O+"),
        'O2': models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method == 'POST':
        bloodForm = forms.BloodForm(request.POST)
        if bloodForm.is_valid():
            bloodgroup = bloodForm.cleaned_data['bloodgroup']
            stock = models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit = bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request, 'blood/admin_blood.html', context=dict)


@login_required(login_url='adminlogin')
def admin_add_hospital(request):
    form = HospitalServiceForm()
    if request.method == 'POST':
        form = HospitalServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data saved successfully")
            return redirect('admin_add_hospital')
    else:
        form = HospitalServiceForm()
    context = {
        'form': form
    }
    return render(request, 'blood/admin_add_hospital.html', context)


@login_required(login_url='adminlogin')
def admin_blood_test_lab(request):
    if request.method == 'POST':
        try:
            donalId = int(request.POST.get('getId'))
            donors = dmodels.BloodDonate.objects.get(donor__id=donalId)
            return redirect('blood_test_result', id=donors.id)
        except:
            messages.error(request, "please make sure that Id is number or Donal is available")
            return render(request, 'blood/admin_blood_test_lab.html')
    return render(request, 'blood/admin_blood_test_lab.html')


@login_required(login_url='adminlogin')
def blood_test_result(request, id):
    donors = dmodels.BloodDonate.objects.get(donor__id=id)
    is_checked = None
    try:
        lab_checked = LabResult.objects.get(donor=donors.donor)
        is_checked = True
    except:
        is_checked = False

    form = LabResultForm()
    if request.method == 'POST':
        form = LabResultForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.donor = donors.donor
            instance.save()
            messages.success(request, "blood checked")
            return redirect('blood_test_result', id=donors.id)
    else:
        form = LabResultForm()
    context = {
        'user_donors': donors,
        'form': form,
        'is_checked': is_checked
    }
    return render(request, 'blood/blood_test_result.html', context)


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors = dmodels.Donor.objects.all()
    return render(request, 'blood/admin_donor.html', {'donors': donors})


def admin_donor_view_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=report' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    request_report = dmodels.Donor.objects.all()
    html_string = render_to_string('pdf/admin_donor_report.html', {'request_report': request_report})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(
            0)  # we fixed this issues by commenting that output = open(output.name, 'rb')  PermissionError at /generate-pdf [Errno 13] Permission denied weasyprint
        # output = open(output.name, 'rb')  # if we run this we got proble error related to the protection on c:/user/oscar
        response.write(output.read())
    return response


@login_required(login_url='adminlogin')
def update_donor_view(request, pk):
    donor = dmodels.Donor.objects.get(id=pk)
    user = dmodels.User.objects.get(id=donor.user_id)
    userForm = dforms.DonorUserForm(instance=user)
    donorForm = dforms.DonorForm(request.FILES, instance=donor)
    mydict = {'userForm': userForm, 'donorForm': donorForm}
    if request.method == 'POST':
        userForm = dforms.DonorUserForm(request.POST, instance=user)
        donorForm = dforms.DonorForm(request.POST, request.FILES, instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            donor = donorForm.save(commit=False)
            donor.user = user
            donor.email = donorForm.cleaned_data['email']
            donor.save()
            return redirect('admin-donor')
    return render(request, 'blood/update_donor.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request, pk):
    donor = dmodels.Donor.objects.get(id=pk)
    user = User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')


@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients = pmodels.Patient.objects.all()
    return render(request, 'blood/admin_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
def update_patient_view(request, pk):
    patient = pmodels.Patient.objects.get(id=pk)
    user = pmodels.User.objects.get(id=patient.user_id)
    userForm = pforms.PatientUserForm(instance=user)
    patientForm = pforms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = pforms.PatientUserForm(request.POST, instance=user)
        patientForm = pforms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.bloodgroup = patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request, 'blood/update_patient.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_patient_view(request, pk):
    patient = pmodels.Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')


@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests = models.BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'blood/admin_request.html', {'requests': requests})


@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests = models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request, 'blood/admin_request_history.html', {'requests': requests})

@login_required(login_url='adminlogin')
def lab_test(request):
    lab_res = LabResult.objects.all()
    context = {
        'lab_res': lab_res
    }
    return render(request, 'blood/lab_test.html', context)


@login_required(login_url='adminlogin')
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=report' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    request_report = models.BloodRequest.objects.all().exclude(status='Pending')
    html_string = render_to_string('pdf/pdf-output.html', {'request_report': request_report})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(
            0)  # we fixed this issues by commenting that output = open(output.name, 'rb')  PermissionError at /generate-pdf [Errno 13] Permission denied weasyprint
        # output = open(output.name, 'rb')  # if we run this we got proble error related to the protection on c:/user/oscar
        response.write(output.read())
    return response


@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations = dmodels.BloodDonate.objects.all()
    lab_checked = dmodels.LabResult.objects.all()
    return render(request, 'blood/admin_donation.html', {'donations': donations, 'lab_checked': lab_checked})


@login_required(login_url='adminlogin')
def blood_donation_detail_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=report' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    blood_donation_report = dmodels.BloodDonate.objects.all()
    html_string = render_to_string('pdf/blood_donation_detail.html', {'blood_donation_report': blood_donation_report})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(
            0)  # we fixed this issues by commenting that output = open(output.name, 'rb')  PermissionError at /generate-pdf [Errno 13] Permission denied weasyprint
        # output = open(output.name, 'rb')  # if we run this we got proble error related to the protection on c:/user/oscar
        response.write(output.read())
    return response


@login_required(login_url='adminlogin')
def update_approve_status_view(request, pk):
    req = models.BloodRequest.objects.get(id=pk)
    message = None
    bloodgroup = req.bloodgroup
    unit = req.unit
    stock = models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit = stock.unit - unit
        stock.save()
        req.status = "Approved"

    else:
        message = "Stock Doest Not Have Enough Blood To Approve This Request, Only " + str(
            stock.unit) + " Unit Available"
    req.save()

    requests = models.BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'blood/admin_request.html', {'requests': requests, 'message': message})


@login_required(login_url='adminlogin')
def update_reject_status_view(request, pk):
    req = models.BloodRequest.objects.get(id=pk)
    req.status = "Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')


@login_required(login_url='adminlogin')
def approve_donation_view(request, pk):
    donation = dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group = donation.bloodgroup
    donation_blood_unit = donation.unit

    stock = models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit = stock.unit + donation_blood_unit
    stock.save()

    donation.status = 'Approved'
    donation.save()
    message_donor = f"Hello {donation.donor} Thank you for donating your blood is approved"
    phone_donor = donation.donor.mobile

    try:
        send_sms(message_donor, phone_donor)
    except:
        pass
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request, pk):
    donation = dmodels.BloodDonate.objects.get(id=pk)
    donation.status = 'Rejected'
    donation.save()
    message_donor = f"Hello {donation.donor} Thank you for donating your blood is rejected"
    phone_donor = donation.donor.mobile

    try:
        send_sms(message_donor, phone_donor)
    except:
        pass
    return HttpResponseRedirect('/admin-donation')
