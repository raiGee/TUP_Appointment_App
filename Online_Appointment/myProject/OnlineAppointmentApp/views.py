from pkgutil import get_data
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa

def Home(request):
    return render(request,"Appointment/Home.html")

def A_login(request):
    if request.user.is_authenticated:
        return redirect ('Access-Table-View')
    else:
        if request.method == 'POST':
            userrr = request.POST.get('username')
            passw = request.POST.get('password') 
            user = authenticate(request, username=userrr,password=passw)
 
            if user is not None:
                login(request, user)
                return redirect ('Access-Table-View')
            else:
                messages.info(request,'Username/Password is incorrect')

    return render(request,"Appointment/A-login.html")

def A_register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        form.instance.is_superuser = True
        if form.is_valid():
            form.save()
            return redirect('alogin')

    return render(request,"Appointment/A-Register.html")

def U_login(request):
    formReg = RegisterForm(request.POST or None)
    userdb = Registration.objects.values_list('username', flat=True)
    passwrd_db = Registration.objects.values_list('passwords', flat=True)

    if formReg.is_valid():
        formReg.save()

    usernames = request.POST.get('user')
    passto = request.POST.get('pass')

    for i in range(len(userdb)):
        if userdb[i] == usernames and passwrd_db[i] == passto:
            request.session['username'] = usernames
            return redirect('form')
    
    return render(request, 'Appointment/U-login.html')


   # return render(request,"Appointment/U-login.html")

def Form(request):
    getusername = request.session['username']
    checkForm = Registration.objects.filter(username=getusername).values()
    appointment = AppointmentForm(request.POST or None)

    if appointment.is_valid():
        messages.info(request,'Successfully Submitted!')
        appointment.save()


    listto = []
    for x in checkForm:
        listto.append(x)

    context = {
        'allData': listto
    }
    return render(request,"Appointment/form.html", context)

def Table(request):
    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        time = request.POST.get('time')

        data = {
                'subject' : subject,
                'time' : time,
                'message' : message,
        }
        message = '''
        New Message : {}

        Time and Date : {}
        '''.format(data['message'], data['time'])
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        return render(
            request,
            'Appointment\Access-Table-View.html',
            {
                'title':'send an email'
            }
        )
    getData = Appointment.objects.all()
  
    context = {
        'data': getData
    }
    return render(request,"Appointment/Access-Table-View.html", context)

def generate(request):
    showData = Appointment.objects.all()

    context = {
        'showData': showData
    }
    return render(request,"Appointment/GenerateTable.html", context)

def pdf_appointment_create(request):
    getData = Appointment.objects.all()

    template_path = 'Appointment/GenerateTable.html'

    context = {'showData': getData}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="appointments.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Table_delete(request, delete_id):
    get_data = Appointment.objects.get(id=delete_id)
    table_del = Appointment.objects.get(id=delete_id)

    context = {
        "del": get_data
    }

    if request.method == "POST":
        table_del.delete()
        return redirect('Access-Table-View')

    return render(request, "Appointment/delete_data.html", context)

def logoutUser(request):
    logout(request)
    return redirect('alogin')


