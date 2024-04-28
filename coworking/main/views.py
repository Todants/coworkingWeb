from django.shortcuts import render
from .models import Businesses
from django.http import JsonResponse


def index(request):
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
    if request.POST:
        form_type = request.POST.get('form_type_btn')
        if form_type == 'company':
            company_name = request.POST.get('company_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone')
            password1 = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            company_name_exists, email_exists, phone_number_exists, password_exists = True, True, True, True
            tempD = {}
            if Businesses.objects.filter(company_name=company_name).exists():
                company_name_exists = False
                tempD['company_name'] = 'company_name'

            if Businesses.objects.filter(email=email).exists():
                email_exists = False
                tempD['email'] = 'email'

            if Businesses.objects.filter(phone_number=phone_number).exists():
                phone_number_exists = False
                tempD['phone'] = 'phone'

            if password1 != password2:
                password_exists = False
                tempD['password'] = 'password'

            if not(company_name_exists and email_exists and phone_number_exists and password_exists):
                return JsonResponse({'error': tempD}, status=400)

            Businesses.objects.create(
                company_name=company_name,
                email=email,
                password=password1,
                phone_number=phone_number
            )

            return JsonResponse({'success': 'User created successfully'}, status=201)

    return render(request, 'main/registration.html')


def temp(request):
    return render(request, 'main/registration.html')


def coworking(request):
    return render(request, 'main/temp_coworking.html')
