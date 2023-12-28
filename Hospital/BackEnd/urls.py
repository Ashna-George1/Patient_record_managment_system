from django.urls import path
from BackEnd import views


urlpatterns = [
        path('Index_Page',views.Index_Page,name="Index_Page"),
        path('AddHospital_Page',views.AddHospital_Page,name="AddHospital_Page"),
        path('AddHospital_data',views.AddHospital_data,name="AddHospital_data"),
        path('AddSpecialization_page',views.AddSpecialization_page,name="AddSpecialization_page"),
        path('AddSpecialisation_data',views.AddSpecialisation_data,name="AddSpecialisation_data"),
        path('Admin_login',views.Admin_login,name="Admin_login"),
        path('Admin_Logout',views.Admin_Logout,name="Admin_Logout"),
        path('Admin_Login_Page',views.Admin_Login_Page,name="Admin_Login_Page"),
        path('admin_hospital_list',views.admin_hospital_list,name="admin_hospital_list"),
        path('admin_doctor_list',views.admin_doctor_list,name="admin_doctor_list"),
        path('admin_patient_list',views.admin_patient_list,name="admin_patient_list"),
        path('admin_lab_report_page',views.admin_lab_report_page,name="admin_lab_report_page"),
        path('admin_OP_History_page',views.admin_OP_History_page,name="admin_OP_History_page"),
        path('admin_doctor_page',views.admin_doctor_page,name="admin_doctor_page"),
        path('admin_contact',views.admin_contact,name="admin_contact"),
        path('admin_upate_doctor_page/<int:doctor_id>/',views.admin_upate_doctor_page,name="admin_upate_doctor_page"),
        path('admin_hospital_delete/<int:hospital_id>/',views.admin_hospital_delete,name="admin_hospital_delete"),
        path('admin_upate_Hospital_page/<int:H_id>/',views.admin_upate_Hospital_page,name="admin_upate_Hospital_page"),
        path('admin_doctor_delete/<int:doctor_id>/',views.admin_doctor_delete,name="admin_doctor_delete"),
        path('admin_labreport_delete/<int:doctor_id>/',views.admin_labreport_delete,name="admin_labreport_delete"),
        path('admin_OP_delete/<int:doctor_id>/',views.admin_OP_delete,name="admin_OP_delete"),
        path('admin_contact_delete/<int:doctor_id>/',views.admin_contact_delete,name="admin_contact_delete"),
        path('admin_patient_delete/<int:doctor_id>/',views.admin_patient_delete,name="admin_patient_delete"),
        path('admin_update_patient_list/<int:patient_id>/',views.admin_update_patient_list,name="admin_update_patient_list"),
        path('Admin_searchresult/',views.Admin_searchresult,name="Admin_searchresult"),
        path('admin_update_doctor_data/<int:did>/',views.admin_update_doctor_data,name="admin_update_doctor_data"),
        path('admin_update_hospital_data/<int:did>/',views.admin_update_hospital_data,name="admin_update_hospital_data"),


]

