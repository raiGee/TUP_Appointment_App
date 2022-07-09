from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Home', views.Home, name='Home'),
    path('A-Login', views.A_login, name='alogin'),
    path('A-Register', views.A_register, name='areg'),
    path('U-Login', views.U_login, name='ulogin'),
    path('form', views.Form, name='form'),
    path('Access-Table-View', views.Table, name='Access-Table-View'),
    path('logout', views.logoutUser, name="logout"),
    path('delete_data/<delete_id>', views.Table_delete, name="delete"),
    path('createPdf', views.pdf_appointment_create, name="createPdf"),
    path('showData', views.generate, name="showData")
]