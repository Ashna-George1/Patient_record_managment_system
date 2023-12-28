
from django.urls import path
from FrontEnd import views
from .views import QuoteList, search_results

urlpatterns = [
        path('',views.Patient_Doctor_Page,name="Patient_Doctor_Page"),
        path('Doctor_SignUp_SignIn_Page/',views.Doctor_SignUp_SignIn_Page,name="Doctor_SignUp_SignIn_Page"),
        path('doctor_Signup_Data/',views.doctor_Signup_Data,name="doctor_Signup_Data"),

        path('Doctor_Login_page/',views.Doctor_Login_page,name="Doctor_Login_page"),
        path('Doctor_Login_Data/',views.Doctor_Login_Data,name="Doctor_Login_Data"),
        path('Doctor_Logout/',views.Doctor_Logout,name="Doctor_Logout"),
        path('Doctor_Dashbord_page/',views.Doctor_Dashbord_page,name="Doctor_Dashbord_page"),
        path('Doctor_PatientInfo_Page/',views.Doctor_PatientInfo_Page,name="Doctor_PatientInfo_Page"),
        path('Doctor_PAtientDetails_page/',views.Doctor_PAtientDetails_page,name="Doctor_PAtientDetails_page"),
        path('Doctor_PatientInfo_Data/<name>/',views.Doctor_PatientInfo_Data,name="Doctor_PatientInfo_Data"),
        path('Doctor_Patient_Medicine/',views.Doctor_Patient_Medicine,name="Doctor_Patient_Medicine"),
        path('Doctor_SignUp_Page/',views.Doctor_SignUp_Page,name="Doctor_SignUp_Page"),
        path('MedicineData/',views.MedicineData,name="MedicineData"),
        path('searchresult/',views.searchresult,name="searchresult"),
        path('Lab_searchresult/',views.Lab_searchresult,name="Lab_searchresult"),
        path('Hospital_contacts/',views.Hospital_contacts,name="Hospital_contacts"),
        path('patient_contacts/',views.patient_contacts,name="patient_contacts"),
        path('ADD_LabReport/<int:pk>/',views.ADD_LabReport,name="ADD_LabReport"),
        path('medicine_delete/<int:med_id>/',views.medicine_delete,name="medicine_delete"),
        path('labprescription_delete/<int:lab_id>/',views.labprescription_delete,name="labprescription_delete"),
        path('patient_labreport_delete/<int:rid>/',views.patient_labreport_delete,name="patient_labreport_delete"),
        path('download_file/<int:file_id>/',views.download_file,name="download_file"),
        path('Lab_Prescription_Data/',views.Lab_Prescription_Data,name="Lab_Prescription_Data"),
        path('LabPrescriptionHistory/',views.LabPrescriptionHistory,name="LabPrescriptionHistory"),
        path("", QuoteList.as_view(), name="all_quotes"),
        path("search_results/", search_results.as_view(), name="search_results"),
        # path("MedicineData/", MedicineData.as_view(), name="MedicineData"),


        path('Patient_Signup_Page/',views.Patient_Signup_Page,name="Patient_Signup_Page"),
        path('Patient_signup_data/',views.Patient_signup_data,name="Patient_signup_data"),
        path('Patient_Login_Page/',views.Patient_Login_Page,name="Patient_Login_Page"),
        path('Patient_Login_Data/',views.Patient_Login_Data,name="Patient_Login_Data"),
        path('Patient_Logout/',views.Patient_Logout,name="Patient_Logout"),
        path('Patient_lab_report_page/',views.Patient_lab_report_page,name="Patient_lab_report_page"),
        path('Patient_op_history_page/',views.Patient_op_history_page,name="Patient_op_history_page"),
        path('Patient_pending_lab_history_page/',views.Patient_pending_lab_history_page,name="Patient_pending_lab_history_page"),



        path('Hospital_Login_Pape/',views.Hospital_Login_Pape,name="Hospital_Login_Pape"),
        path('Hospital_Signup_Pape/',views.Hospital_Signup_Pape,name="Hospital_Signup_Pape"),
        path('Hospital_Dashbord_Pape/',views.Hospital_Dashbord_Pape,name="Hospital_Dashbord_Pape"),
        path('Laboratory_Page/',views.Laboratory_Page,name="Laboratory_Page"),
        path('Hospital_Signup_Data/',views.Hospital_Signup_Data,name="Hospital_Signup_Data"),
        path('Hospital_Login_Data/',views.Hospital_Login_Data,name="Hospital_Login_Data"),
        path('Hospital_Logout/',views.Hospital_Logout,name="Hospital_Logout"),
]
