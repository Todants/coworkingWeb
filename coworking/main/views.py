from django.shortcuts import render
from .models import Businesses


def index(request):
    if request.POST:

        form_type = request.POST.get('form_type_btn')
        if form_type == 'company':

            company_name_exists, email_exists, phone_number_exists, password_exists = False, False, False, False
            company_name = request.POST.get('company_name')
            if company_name:
                company_name_exists = not(Businesses.objects.filter(company_name=company_name).exists())
            email = request.POST.get('email')
            if email:
                email_exists = not(Businesses.objects.filter(email=email).exists())
            phone_number = request.POST.get('phone')
            if phone_number:
                phone_number_exists = not(Businesses.objects.filter(phone_number=phone_number).exists())
            password1 = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            if password1 == password2:
                password_exists = True

            if company_name_exists and email_exists and phone_number_exists and password_exists:
                Businesses.objects.create(
                    company_name=company_name,
                    email=email,
                    password=password1,
                    phone_number=phone_number
                )
            else:
                print('Ошибка при создании компании')

    return render(request, 'main/base.html')


def login(request):
    return render(request, 'main/login.html')


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def profile(request):
    return render(request, 'main/profile.html')


def registration(request):
    return render(request, 'main/registration.html')


def temp(request):
    return render(request, 'main/registration.html')
