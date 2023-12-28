import datetime

from django.shortcuts import render, redirect
from BackEnd.models import HospitalDB, SpecializationDB
from FrontEnd.models import DoctorDB, PatientDB, MedicineDB,ContactDB, PatientDetailsDB, HospitalNewDB,LabPrescriptionDB,LabPrescriptionHistoryDB,LabReportsDB
from itertools import chain
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def Patient_Doctor_Page(PDP):
    return render(PDP, "Patient_Doctor.html")


def Doctor_SignUp_SignIn_Page(PDP):
    hospital = HospitalDB.objects.all()
    specialization = SpecializationDB.objects.all()
    return render(PDP, "doctor/Doctor_Signup.html", {'hospital': hospital, 'specialization': specialization})


def Doctor_SignUp_Page(request):
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    user = ""
    for i in hospital:
        user = i.H_Username
    doctor = DoctorDB.objects.filter(User=user)
    return render(request, "doctor/SignupNew.html", {'hospital': hospital, 'doctor': doctor})


def doctor_Signup_Data(request):
    if request.method == "POST":
        na = request.POST.get('name')
        uq = request.POST.get('q')
        em = request.POST.get('email')
        mob = request.POST.get('mobile')
        hs = request.POST.get('hospital')
        dt = request.POST.get('date')
        cnt = request.POST.get('country')
        sp = request.POST.get('specialization')
        md = request.POST.get('medicalid')
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        img = request.FILES['medical']
        img2 = request.FILES['photo']
        obj = DoctorDB(Name=na, User=uq, Email=em, Mobile=mob, Hospital=hs, Date=dt,
                       Country=cnt, Specialization=sp, Medicalid=md, Username=usr, Password=pwd, Medical=img,
                       Photo=img2)
        obj.save()
        return redirect(Doctor_SignUp_Page)


def Patient_Signup_Page(PDP):
    return render(PDP, "Patient/Patient_Signup.html")


def Patient_signup_data(request):
    if request.method == 'POST':
        fna = request.POST.get('fname')
        lna = request.POST.get('lname')
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        bld = request.POST.get('gender')
        ads = request.POST.get('address')
        mob = request.POST.get('mobile')
        img = request.FILES['image']
        if PatientDB.objects.filter(Username=usr).exists():
            messages.error(request, 'Username already exists')
            return redirect(Patient_Signup_Page)
        else:
            obj = PatientDB(Name=fna, LName=lna, Username=usr, Password=pwd, Gender=bld, Address=ads, Mobile=mob,
                            profile_pic=img)
            obj.save()
            s =  messages.error(request, 'Please Save Your Patient ID : ')
            return render(request, "Patient/Patient_Login.html",{'s':s,'usr':usr})





def Patient_Login_Page(request):
    return render(request, "Patient/Patient_Login.html")


def Patient_Login_Data(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')


        if PatientDB.objects.filter(Username=un, Password=pwd).exists():
            request.session['Username'] = un
            request.session['Password'] = pwd
            patient = PatientDB.objects.filter(Username=un)
            return render(request, "doctor/DashBord.html",{'patient':patient})
        else:
            messages.info(request, 'Invalid login details')
            return redirect(Patient_Login_Page)

    return redirect(Patient_Login_Page)


def Patient_lab_report_page(request):
    lab = LabPrescriptionHistoryDB.objects.filter(Username=request.session['Username']).order_by('date').values()[::-1]
    return render(request,"patient/patient_lab_reports.html",{'lab':lab})

def patient_labreport_delete(request,rid):
    data = LabPrescriptionHistoryDB.objects.get(id=rid)
    data.delete()
    return redirect(Patient_lab_report_page)

def Patient_op_history_page(request):
    op = PatientDetailsDB.objects.filter(Username=request.session['Username']).order_by('date').values()[::-1]
    return render(request,"patient/patient_op_history.html",{'op':op})

def Patient_pending_lab_history_page(request):
    op = LabPrescriptionHistoryDB.objects.filter(Username=request.session['Username'],Status='Pending').order_by('date').values()[::-1]
    return render(request,"patient/patient_pending_lab_reports.html",{'op':op})


def Doctor_Login_page(request):
    return render(request, "doctor/Doctor_Login.html")


def Doctor_Login_Data(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        q = request.POST.get('q')  # hospital Username
        doctor = DoctorDB.objects.filter(User=q)
        for i in doctor:
            if i.Username==un:
                if DoctorDB.objects.filter(Username=un, Password=pwd).exists():
                    request.session['Username'] = un
                    request.session['Password'] = pwd
                    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])

                    doctor = DoctorDB.objects.filter(Username=un)
                    return render(request, "doctor/Doctor_Patientinfo.html", {'doctor': doctor,'hospital':hospital})

                else:
                    return redirect(Doctor_SignUp_Page)

    return redirect(Doctor_SignUp_Page)


def Doctor_Dashbord_page(request):
    patient = PatientDB.objects.filter(Username=request.session['Username'])
    return render(request, "doctor/DashBord.html", {'patient': patient})


def Doctor_PatientInfo_Page(request):
    patient = PatientDB.objects.all()
    return render(request, "doctor/Doctor_Patientinfo.html", {'patient': patient})


def Doctor_PatientInfo_Data(request, name):
    patient = PatientDB.objects.get(Username=name)
    return render(request, "doctor/Doctor_Patientinfo.html", {'patient': patient})


def Doctor_PAtientDetails_page(request):
    patient = PatientDB.objects.all()
    return render(request, "doctor/D_PatientDetails.html", {'patient': patient})


def Hospital_Dashbord_Page(request):
    return render(request, "Hospital/HospitalDashbord.html")


@method_decorator(cache_page(60 * 5), name="dispatch")
class QuoteList(ListView):
    model = PatientDB
    context_object_name = "quotes"
    template_name = "doctor/Doctor_Patientinfo.html"


# SearchVectorField
class search_results(ListView):
    model = PatientDB
    context_object_name = "quotes","y"
    template_name = "doctor/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return PatientDB.objects.filter(Username=query),PatientDetailsDB.objects.filter(Username=query)


def searchresult(request):
    query = request.GET.get("q")
    quotes = PatientDB.objects.filter(Username=query)
    x = MedicineDB.objects.all()
    y = PatientDetailsDB.objects.filter(Username=query).order_by('date').values()[::-1]
    doctor = DoctorDB.objects.filter(Username=request.session['Username'])
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    lab = LabPrescriptionHistoryDB.objects.filter(Username=query).order_by('date').values()[::-1]
    z = LabPrescriptionDB.objects.filter(Username=query).order_by('date')
    medical = MedicineDB.objects.all()
    b = LabPrescriptionDB.objects.all()
    user = ""
    for i in hospital:
        user = i.H_Username
    doctor1 = DoctorDB.objects.filter(User=user)
    if PatientDB.objects.filter(Username=query).exists():
        return render(request, "doctor/search.html",
                      {'quotes': quotes, 'x': x, 'y': y,'doctor1':doctor1, 'z': z,'hospital':hospital, 'doctor': doctor,'lab':lab, 'b': b, 'medical': medical})

    else:
        return redirect(Doctor_PatientInfo_Page)


def MedicineData(request):
    if request.method == "POST":
        na = request.POST.get('medicine')
        n = request.POST.get('q')
        h = request.POST.get('h')
        u = request.POST.get('u')
        dn = request.POST.get('dn')
        mrg = request.POST.get('morning')
        aftr = request.POST.get('afternoon')
        nt = request.POST.get('night')
        d = request.POST.get('day')
        m = request.POST.get('message')
        date = datetime.datetime.now()
        obj = MedicineDB(Medicine=na, Username=n, Hospital_Name=h, Doctor_User=u,Doctor_Name=dn, Morning=mrg, Afternoon=aftr, Night=nt,
                         Day=d, Message=m,date=date)
        obj.save()

        query = request.POST.get("q")
        quotes = PatientDB.objects.filter(Username=query)
        x = MedicineDB.objects.filter(Username=query)
        y = PatientDetailsDB.objects.filter(Username=query).order_by('date').values()[::-1]
        doctor = DoctorDB.objects.filter(Username=request.session['Username'])
        hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
        z = LabPrescriptionDB.objects.filter(Username=query).order_by('date')
        lab = LabPrescriptionHistoryDB.objects.filter(Username=query).order_by('date','-id').values()[::-1]
        medical = MedicineDB.objects.all()
        b = LabPrescriptionDB.objects.all()
        user = ""
        for i in hospital:
            user = i.H_Username
        doctor1 = DoctorDB.objects.filter(User=user)

        if PatientDB.objects.filter(Username=n).exists():
            return render(request, "doctor/search.html",
                          {'quotes': quotes, 'x': x, 'y': y,'doctor1':doctor1, 'z': z,'hospital':hospital, 'doctor':doctor,'lab':lab, 'b': b, 'medical': medical})

        else:
            return redirect(Doctor_PatientInfo_Page)



        # return redirect('search_results',{'quotes':quotes,'x':x})
        # return redirect('search_results')


def Doctor_Patient_Medicine(request):  # save daily doctor medicine report to main db
    if request.method == "POST":
        u = request.POST.get('q')
        n = MedicineDB.objects.all()
        for i in n:
            medicine = i.Medicine
            user = i.Username
            mrg = i.Morning
            aftr = i.Afternoon
            nt = i.Night
            day = i.Day
            m = i.Message
            h = i.Hospital_Name
            u = i.Doctor_User
            dn = i.Doctor_Name
            d = i.date
            y = PatientDetailsDB(Medicine=medicine, Username=user,Hospital_Name=h, Doctor_User=u,Doctor_Name=dn, Morning=mrg, Afternoon=aftr, Night=nt, Day=day,
                                 Message=m,date=d)
            y.save()
        n.delete()
        u = request.POST.get('q')
        quotes = PatientDB.objects.filter(Username=u)
        x = MedicineDB.objects.filter(Username=u)
        y = PatientDetailsDB.objects.filter(Username=u).order_by('date').values()[::-1]
        doctor = DoctorDB.objects.filter(Username=request.session['Username'])
        z = LabPrescriptionDB.objects.filter(Username=u).order_by('date')
        hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
        lab = LabPrescriptionHistoryDB.objects.filter(Username=u).order_by('date','-id').values()[::-1]
        medical = MedicineDB.objects.all()
        b = LabPrescriptionDB.objects.all()
        user = ""
        for i in hospital:
            user = i.H_Username
        doctor1 = DoctorDB.objects.filter(User=user)
        if PatientDB.objects.filter(Username=u).exists():
            return render(request, "doctor/search.html",
                          {'quotes': quotes, 'x': x,'doctor1':doctor1, 'y': y,'hospital':hospital, 'z': z,'doctor':doctor,'lab':lab, 'b': b, 'medical': medical})

        else:
            return redirect(Doctor_PatientInfo_Page)






def Lab_Prescription_Data(request):
    if request.method=="POST":
        n = request.POST.get('q')
        h = request.POST.get('h')
        u = request.POST.get('u')
        dn = request.POST.get('dn')
        m = request.POST.get('message')
        d = datetime.datetime.now()

        obj = LabPrescriptionDB(Username=n,Hospital_Name=h,Doctor_User=u,Doctor_Name=dn,Message=m,date=d)
        obj.save()
        query = request.POST.get("q")
        n = request.POST.get('q')
        quotes = PatientDB.objects.filter(Username=query)
        x = MedicineDB.objects.filter(Username=query)
        y = PatientDetailsDB.objects.filter(Username=query).order_by('date').values()[::-1]
        doctor = DoctorDB.objects.filter(Username=request.session['Username'])
        hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
        z = LabPrescriptionDB.objects.filter(Username=query).order_by('date')
        lab = LabPrescriptionHistoryDB.objects.filter(Username=query).order_by('date','-id').values()[::-1]
        b = LabPrescriptionDB.objects.all()
        medical = MedicineDB.objects.all()
        user = ""
        for i in hospital:
            user = i.H_Username
        doctor1 = DoctorDB.objects.filter(User=user)
        if PatientDB.objects.filter(Username=n).exists():
            return render(request, "doctor/search.html",
                          {'quotes': quotes, 'x': x, 'y': y,'hospital':hospital,'doctor1':doctor1, 'z': z,'doctor':doctor,'lab':lab, 'b': b, 'medical': medical})

        else:
            return redirect(Doctor_PatientInfo_Page)


def LabPrescriptionHistory(request):  # save daily doctor medicine report to main db
    if request.method == "POST":
        u = request.POST.get('q')
        n = LabPrescriptionDB.objects.all()
        for i in n:
            user = i.Username
            m = i.Message
            h = i.Hospital_Name
            u = i.Doctor_User
            d = i.date
            y = LabPrescriptionHistoryDB(Username=user,Hospital_Name=h, Doctor_User=u,
                                 Message=m,date=d)
            y.save()
        n.delete()
        u = request.POST.get('q')
        quotes = PatientDB.objects.filter(Username=u)
        x = MedicineDB.objects.filter(Username=u)
        y = PatientDetailsDB.objects.filter(Username=u).order_by('date').values()[::-1]
        doctor = DoctorDB.objects.filter(Username=request.session['Username'])
        hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
        z = LabPrescriptionDB.objects.filter(Username=u).order_by('date')
        lab = LabPrescriptionHistoryDB.objects.filter(Username=u).order_by('date','-id').values()[::-1]
        b = LabPrescriptionDB.objects.all()
        medical = MedicineDB.objects.all()
        user = ""
        for i in hospital:
            user = i.H_Username
        doctor1 = DoctorDB.objects.filter(User=user)
        if PatientDB.objects.filter(Username=u).exists():
            return render(request, "doctor/search.html",
                          {'quotes': quotes, 'x': x, 'y': y,'doctor1':doctor1,'hospital':hospital, 'z': z,'doctor':doctor,'lab':lab, 'b': b, 'medical': medical})

        else:
            return redirect(Doctor_PatientInfo_Page)


####################################################3

def Hospital_Login_Pape(request):
    return render(request, "Hospitals/Hospital_Login.html")


def Hospital_Login_Data(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        if HospitalNewDB.objects.filter(H_Username=un, H_Password=pwd).exists():
            request.session['H_Username'] = un
            request.session['H_Password'] = pwd
            hospital = HospitalNewDB.objects.filter(H_Username=un)
            # hospital = HospitalNewDB.objects.filter(Username=request.session['Username'])
            doctor = DoctorDB.objects.filter(User=un)
            return render(request, "Hospitals/Hospital_Dashbord.html", {'hospital': hospital,'doctor':doctor})
        else:
            messages.error(request, 'Invalid Username or Password')

            return redirect(Hospital_Login_Pape)

    return redirect(Hospital_Login_Pape)


def Hospital_Signup_Pape(request):
    return render(request, "Hospitals/Hospital_Signup.html")


def Hospital_Signup_Data(request):
    if request.method == "POST":
        na = request.POST.get('name')
        em = request.POST.get('email')
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        cnt = request.POST.get('country')
        sp = request.POST.get('mobile')
        md = request.POST.get('address')
        img = request.FILES['image']


        if HospitalNewDB.objects.filter(H_Username=usr).exists():
            hospital = HospitalNewDB.objects.filter(H_Username=usr)
            # hospital = HospitalNewDB.objects.filter(Username=request.session['Username'])
            doctor = DoctorDB.objects.filter(User=usr)
            messages.error(request, 'Username Already exists')
            return redirect(Hospital_Signup_Pape)
        else:
            obj = HospitalNewDB(Name=na, Email=em, H_Username=usr, H_Password=pwd,
                                Country=cnt, Mobile=sp, Address=md, Img=img)
            obj.save()

            return redirect(Hospital_Login_Pape)

    return redirect(Hospital_Login_Pape)


def Hospital_Dashbord_Pape(request):
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    return render(request, "Hospitals/Hospital_Dashbord.html",{'hospital':hospital})


def Laboratory_Page(request):
    return render(request, "Hospitals/Lab_serach.html")

def Lab_searchresult(request):
    query = request.GET.get("q")
    quotes = PatientDB.objects.filter(Username=query)
    x = MedicineDB.objects.all()
    y = PatientDetailsDB.objects.filter(Username=query).order_by('date')
    z = LabPrescriptionDB.objects.filter(Username=query).order_by('date')
    doctor = DoctorDB.objects.filter(User=request.session['H_Username'])

    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    b = LabPrescriptionHistoryDB.objects.filter(Username=query,Status="Pending").order_by('date','-id').values()[::-1]
    medical = MedicineDB.objects.all()
    b1 = LabPrescriptionHistoryDB.objects.filter(Username=query,Status="Completed").order_by('date','-id').values()[::-1]

    r = LabReportsDB.objects.all()
    r1 = LabReportsDB.objects.filter(P_Username=query).order_by('date','-id').values()[::-1]

    if PatientDB.objects.filter(Username=query).exists():
        return render(request, "Hospitals/Laboratory.html", {'quotes': quotes,'doctor':doctor,'b1':b1,'r':r,'r1':r1, 'x': x, 'y': y,'z':z,'hospital': hospital,'b':b,'medical':medical})

    else:
        return redirect(Laboratory_Page)


def ADD_LabReport(request,pk):
    Lab = LabPrescriptionHistoryDB.objects.get(id=pk)
    pu=Lab.Username
    Lab.Status="Completed"
    Lab.Report = request.FILES['upload']
    Lab.lab = request.POST.get('l')
    Lab.date = datetime.datetime.now()
    Lab.save()

    x = MedicineDB.objects.all()
    y = PatientDetailsDB.objects.filter(Username=pu).order_by('date')
    z = LabPrescriptionDB.objects.filter(Username=pu).order_by('date')
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    doctor = DoctorDB.objects.filter(User=request.session['H_Username'])

    b = LabPrescriptionHistoryDB.objects.filter(Username=pu,Status="Pending").order_by('date','-id').values()[::-1]
    r = LabReportsDB.objects.all()
    b1 = LabPrescriptionHistoryDB.objects.filter(Username=pu,Status="Completed").order_by('date','-id').values()[::-1]
    r1 = LabReportsDB.objects.filter(P_Username=pu).order_by('date','-id').values()[::-1]
    medical = MedicineDB.objects.all()
    quotes = PatientDB.objects.filter(Username=pu)

    return render(request, "Hospitals/Laboratory.html",
                      {'quotes': quotes,'doctor':doctor,'r':r,'r1':r1,'b1':b1, 'x': x, 'y': y, 'z': z, 'hospital': hospital, 'b': b, 'medical': medical})



def download_file(request, file_id):
    uploaded_file = LabPrescriptionHistoryDB.objects.get(id=file_id)
    response = HttpResponse(uploaded_file.Report, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.Report.name}"'
    return response



def Doctor_Logout(request):
    del request.session['Username']
    del request.session['Password']
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    user = ""
    for i in hospital:
        user = i.H_Username
    doctor = DoctorDB.objects.filter(User=user)
    return render(request, "doctor/SignupNew.html", {'hospital': hospital, 'doctor': doctor})

def Hospital_Logout(request):
    del request.session['H_Username']
    del request.session['H_Password']
    return redirect(Patient_Doctor_Page)

def Patient_Logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(Patient_Doctor_Page)

def medicine_delete(request,med_id):
    data = MedicineDB.objects.get(id=med_id)
    u = data.Username
    data.delete()
    u = data.Username
    quotes = PatientDB.objects.filter(Username=u)
    x = MedicineDB.objects.filter(Username=u)
    y = PatientDetailsDB.objects.filter(Username=u).order_by('date')
    doctor = DoctorDB.objects.filter(Username=request.session['Username'])
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    z = LabPrescriptionDB.objects.filter(Username=u).order_by('date')
    lab = LabPrescriptionHistoryDB.objects.filter(Username=u).order_by('date', '-id').values()[::-1]
    b = LabPrescriptionDB.objects.all()
    medical = MedicineDB.objects.all()
    user = ""
    for i in hospital:
        user = i.H_Username
    doctor1 = DoctorDB.objects.filter(User=user)

    return render(request, "doctor/search.html",
                  {'quotes': quotes, 'x': x, 'y': y,'doctor1':doctor1, 'hospital': hospital, 'z': z, 'doctor': doctor, 'lab': lab, 'b': b,
                   'medical': medical})


def labprescription_delete(request,lab_id):
    data = LabPrescriptionDB.objects.get(id=lab_id)
    u = data.Username
    data.delete()
    u = data.Username
    quotes = PatientDB.objects.filter(Username=u)
    x = MedicineDB.objects.filter(Username=u)
    y = PatientDetailsDB.objects.filter(Username=u).order_by('date')
    doctor = DoctorDB.objects.filter(Username=request.session['Username'])
    hospital = HospitalNewDB.objects.filter(H_Username=request.session['H_Username'])
    z = LabPrescriptionDB.objects.filter(Username=u).order_by('date')
    lab = LabPrescriptionHistoryDB.objects.filter(Username=u).order_by('date', '-id').values()[::-1]
    b = LabPrescriptionDB.objects.all()
    medical = MedicineDB.objects.all()
    user = ""
    for i in hospital:
        user = i.H_Username
    doctor1 = DoctorDB.objects.filter(User=user)

    return render(request, "doctor/search.html",
                  {'quotes': quotes, 'x': x, 'y': y,'doctor1':doctor1,'hospital': hospital, 'z': z, 'doctor': doctor, 'lab': lab, 'b': b,
                   'medical': medical})


def patient_contacts(request):
    if request.method=="POST":
        n = request.POST.get('name')
        e = request.POST.get('email')
        s = request.POST.get('subject')
        m = request.POST.get('message')
        d = datetime.datetime.now()

        obj = ContactDB(Name=n,Email=e,Subject=s,Message=m,date=d)
        obj.save()
        return redirect(Doctor_Dashbord_page)
def Hospital_contacts(request):
    if request.method=="POST":
        n = request.POST.get('name')
        e = request.POST.get('email')
        s = request.POST.get('subject')
        m = request.POST.get('message')
        d = datetime.datetime.now()

        obj = ContactDB(Name=n,Email=e,Subject=s,Message=m,date=d)
        obj.save()
        return redirect(Hospital_Dashbord_Pape)