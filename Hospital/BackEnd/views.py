from django.shortcuts import render,redirect
from BackEnd.models import HospitalDB,SpecializationDB
from FrontEnd.models import HospitalNewDB,MedicineDB,ContactDB,LabPrescriptionHistoryDB,LabReportsDB,LabPrescriptionDB,DoctorDB,PatientDB,LabPrescriptionHistoryDB,PatientDetailsDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from FrontEnd.views import Patient_Doctor_Page
# Create your views here.

def Index_Page(ip):
    return render(ip,"Index.html")

def Admin_Logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(Patient_Doctor_Page)

def Admin_searchresult(request):
    query = request.GET.get("q")
    quotes = PatientDB.objects.filter(Username=query)
    x = MedicineDB.objects.all()
    y = PatientDetailsDB.objects.filter(Username=query).order_by('date')
    lab = LabPrescriptionHistoryDB.objects.filter(Username=query).order_by('date','-id').values()[::-1]
    z = LabPrescriptionDB.objects.filter(Username=query).order_by('date')
    medical = MedicineDB.objects.all()
    b = LabPrescriptionDB.objects.all()

    if PatientDB.objects.filter(Username=query).exists():
        return render(request, "adminsearch.html",
                      {'quotes': quotes, 'x': x, 'y': y, 'z': z,'lab':lab, 'b': b, 'medical': medical})

    else:
        return redirect(Index_Page)



def AddHospital_Page(ahp):
    return render(ahp,"AddHospitals.html")

def AddHospital_data(ad):
    if ad.method=="POST":
        hna = ad.POST.get('hname')
        lcn = ad.POST.get('location')
        ds = ad.POST.get('description')
        himg = ad.FILES['image']
        obj = HospitalDB(Hosp_Name=hna,Location=lcn,Description=ds,Hosp_Image=himg)
        obj.save()
        return redirect(AddHospital_Page)

def AddSpecialization_page(ap):
    return render(ap,"AddSpecialization.html")

def AddSpecialisation_data(ad):
    if ad.method=="POST":
        spcl = ad.POST.get('specialization')
        obj = SpecializationDB(Specialization=spcl)
        obj.save()
        return redirect(AddSpecialization_page)


def Admin_Login_Page(request):
    return render(request,"Admin_login.html")

def Admin_login(request):
    if request.method=="POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        if User.objects.filter(username__contains=un).exists():
            user = authenticate(username=un,password=pwd)
            if User is not None:
                login(request,user)
                request.session['username']=un
                request.session['password']=pwd
                return redirect(Index_Page)
            else:
                return redirect(Admin_Login_Page)
        else:
            return redirect(Admin_Login_Page)

def admin_hospital_list(request):
    x = HospitalNewDB.objects.all()
    return render(request,"Admin_hospitals_list.html",{'x':x})

def admin_upate_Hospital_page(request,H_id):
    x = HospitalNewDB.objects.get(id=H_id)
    return render(request,"admin_update_hospital_page.html",{'x':x})

def admin_hospital_delete(request,hospital_id):
    data = HospitalNewDB.objects.get(id=hospital_id)
    data.delete()
    messages.error(request, "data Delete successfully..!")
    return redirect(admin_hospital_list)

def admin_doctor_list(request):
    x = DoctorDB.objects.all()
    return render(request,"Admin_doctors_list.html",{'x':x})

def admin_doctor_delete(request,doctor_id):
    data = HospitalNewDB.objects.get(id=doctor_id)
    data.delete()
    messages.error(request, " Delete successfully..!")
    return redirect(admin_doctor_list)


def admin_patient_delete(request,doctor_id):
    data = PatientDB.objects.get(id=doctor_id)
    data.delete()
    messages.success(request, " Delete successfully..!")
    return redirect(admin_patient_list)

def admin_labreport_delete(request,doctor_id):
    data = LabPrescriptionHistoryDB.objects.get(id=doctor_id)
    data.delete()
    messages.success(request, " Delete successfully..!")
    return redirect(admin_lab_report_page)

def admin_OP_delete(request,doctor_id):
    data = PatientDetailsDB.objects.get(id=doctor_id)
    data.delete()
    messages.success(request, " Delete successfully..!")
    return redirect(admin_OP_History_page)

def admin_patient_list(request):
    x = PatientDB.objects.all()
    return render(request,"Admin_patients_list.html",{'x':x})

def admin_update_patient_list(request,patient_id):
    x = PatientDB.objects.get(Username=patient_id)
    return render(request,"Admin_update_patients_details.html",{'x':x})

def admin_lab_report_page(request):
    x = LabPrescriptionHistoryDB.objects.all()
    return render(request,"Admin_Lab_reports.html",{'x':x})

def admin_OP_History_page(request):
    x = PatientDetailsDB.objects.all()
    return render(request,"OP Details.html",{'x':x})

def admin_doctor_page(request):
    x = DoctorDB.objects.all()
    return render(request,"Admin_Hospitals.html",{'x':x})

def admin_upate_doctor_page(request,doctor_id):
    x = DoctorDB.objects.get(id=doctor_id)
    return render(request,"Admin_update_doctor.html",{'x':x})

def admin_update_doctor_data(request,did):
    data = DoctorDB.objects.get(id=did)
    data.Name = request.POST.get('fname')
    data.Email = request.POST.get('email')
    data.Mobile = request.POST.get('mobile')
    data.Country = request.POST.get('country')

    try:
        img = request.FILES['image']
        fs = FileSystemStorage()
        data.Photo = fs.save(img.name, img)
    except MultiValueDictKeyError:
        data.Photo = DoctorDB.objects.get(id=did).Photo
    data.save()
    return redirect(admin_doctor_list)

def admin_update_hospital_data(request,did):
    data = HospitalNewDB.objects.get(id=did)
    data.Name = request.POST.get('fname')
    data.Email = request.POST.get('email')
    data.Address = request.POST.get('address')
    data.Mobile = request.POST.get('mobile')
    data.Country = request.POST.get('country')

    try:
        img = request.FILES['image']
        fs = FileSystemStorage()
        data.Img = fs.save(img.name, img)
    except MultiValueDictKeyError:
        data.Img = DoctorDB.objects.get(id=did).Photo
    data.save()
    return redirect(admin_hospital_list)

def admin_contact(request):
    contact = ContactDB.objects.all()
    return render(request,"admin_contacts.html",{'contact':contact})


def admin_contact_delete(request,doctor_id):
    data = ContactDB.objects.get(id=doctor_id)
    data.delete()
    messages.success(request, "Contacts Delete successfully..!")
    return redirect(admin_contact)