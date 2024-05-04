from django.shortcuts import render
from .models import Businesses, Users
from django.http import JsonResponse
from datetime import datetime


# def header_insert(request):
#     user_info = request.session.get('user_info', [])
#     if user_info:
#         authorize_check = 'main/base_logged_in.html'
#     else:
#         authorize_check = 'main/base.html'
#     if len(user_info) == 3 and user_info[2] !=
#     original_result[2]['authorize_check'] = authorize_check
#     return original_result


def index(request):
    # request.session['user_info'] = []
    user_info = request.session.get('user_info', [])
    if user_info:
        user_email = user_info[0]
        user_data = None
        if Users.objects.filter(email=user_email).exists():
            user_data = Users.objects.get(email=user_email)
        elif Businesses.objects.filter(email=user_email).exists():
            user_data = Businesses.objects.get(email=user_email)

        if user_data:
            print("Email:", user_email)
            return render(request, 'main/base_logged_in.html')
        else:
            print("Разлогинило")
            request.session['user_info'] = []
    return render(request, 'main/base.html')


def login_view(request):
    if request.POST:

        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data = None
        if Users.objects.filter(email=email, password=password).exists():
            user_data = Users.objects.get(email=email)
        elif Businesses.objects.filter(email=email, password=password).exists():
            user_data = Businesses.objects.get(email=email)

        if user_data:
            request.session['user_info'] = [email, password]
            return JsonResponse({'success': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'error': {'unlog': 'unlog'}}, status=400)

    return render(request, 'main/login.html')


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    user_info = request.session.get('user_info', [])
    if user_info:
        authorize_check = 'main/base_logged_in.html'
    else:
        request.session = None
        authorize_check = 'main/base.html'
    return [request, 'main/contacts.html', {'authorize_check': authorize_check}]


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

            if not (company_name_exists and email_exists and phone_number_exists and password_exists):
                return JsonResponse({'error': tempD}, status=400)

            Businesses.objects.create(
                company_name=company_name,
                email=email,
                password=password1,
                phone_number=phone_number
            )
            request.session['user_info'] = [email, password1]

            return JsonResponse({'success': 'User created successfully'}, status=201)

        elif form_type == 'user':
            email = request.POST.get('email2')
            password = request.POST.get('password2')
            confirm_password = request.POST.get('confirm_password2')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone2')

            date_of_birth = request.POST.get('birth')
            parsed_date = datetime.strptime(date_of_birth, '%d.%m.%Y')
            date_of_birth = parsed_date.strftime('%Y-%m-%d')

            email_exists, phone_number_exists, password_exists = True, True, True
            tempD = {}

            if Businesses.objects.filter(email=email).exists():
                email_exists = False
                tempD['email'] = 'email'

            if Businesses.objects.filter(phone_number=phone_number).exists():
                phone_number_exists = False
                tempD['phone'] = 'phone'

            if password != confirm_password:
                password_exists = False
                tempD['password'] = 'password'

            if not (email_exists and phone_number_exists and password_exists):
                return JsonResponse({'error': tempD}, status=400)

            Users.objects.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth
            )
            request.session['user_info'] = [email, password]
            return JsonResponse({'success': 'User created successfully'}, status=201)

    return render(request, 'main/registration.html')


def temp(request):
    return render(request, 'main/registration.html')


def coworking(request):
    return render(request, 'main/temp_coworking.html')
