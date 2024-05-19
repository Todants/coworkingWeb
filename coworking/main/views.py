import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Businesses, Users, Services, CoworkingSpaces, Images, Bookings
from django.http import JsonResponse
from datetime import datetime


def index(request):
    user_info = request.session.get('user_info', [])
    acc = None
    if user_info:
        authorize_check = 'main/base_logged_in.html'
        acc = Businesses.objects.filter(email=user_info[0]).first()
        if not acc:
            acc = Users.objects.filter(email=user_info[0]).first()
    else:
        authorize_check = 'main/base.html'

    cowork = {}
    coworkings = CoworkingSpaces.objects.all()
    for i in coworkings:
        images = Images.objects.filter(id_coworking=i.id)
        cowork[i.id] = {'name': i.coworking_name, 'rating': i.rating, 'image': images[0].file}

    context = {'authorize_check': authorize_check, 'coworkings': cowork, 'avatar': acc.img if acc else None}

    return render(request, 'main/book.html', context)


def login_view(request):
    if request.method == 'POST' and request.POST.get('logout') == 'true':
        request.session['user_info'] = []
        return redirect(reverse('login_view'))
    elif request.POST:

        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data = None
        if Users.objects.filter(email=email, password=password).exists():
            user_data = Users.objects.get(email=email)
        elif Businesses.objects.filter(email=email, password=password).exists():
            user_data = Businesses.objects.get(email=email)

        if user_data:
            request.session['user_info'] = [email]
            return JsonResponse({'success': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'error': {'unlog': 'unlog'}}, status=400)

    return render(request, 'main/login.html')


def about(request):
    user_info = request.session.get('user_info', [])
    acc = None
    if user_info:
        authorize_check = 'main/base_logged_in.html'
        acc = Businesses.objects.filter(email=user_info[0]).first()
        if not acc:
            acc = Users.objects.filter(email=user_info[0]).first()
    else:
        authorize_check = 'main/base.html'

    return render(request, 'main/about.html', {'authorize_check': authorize_check, 'avatar': acc.img if acc else None})


def create_coworking(request):
    user_info = request.session.get('user_info', [])

    if user_info:
        acc = Businesses.objects.filter(email=user_info[0]).first()
        if not acc:
            return redirect(reverse('profile'))
    else:
        return redirect(reverse('login_view'))
    if request.POST:
        com_name = request.POST.get('text1')
        description = request.POST.get('text2')
        address = request.POST.get('text3')
        files = request.FILES.getlist('file')
        avatar_fields = ['avatar1', 'avatar2', 'avatar3', 'avatar4', 'avatar5']

        temp_co = CoworkingSpaces.objects.create(
            id_company=acc,
            coworking_name=com_name,
            description=description,
            address=address
        )
        print(temp_co)
        for field in avatar_fields:
            if field in request.FILES:
                Images.objects.create(id_coworking=temp_co, file=request.FILES[field])

        return redirect(reverse('profile'))

    return render(request, 'main/create_coworking.html', {'avatar': acc.img})


def contacts(request):
    user_info = request.session.get('user_info', [])
    acc = None
    if user_info:
        authorize_check = 'main/base_logged_in.html'
        acc = Businesses.objects.filter(email=user_info[0]).first()
        if not acc:
            acc = Users.objects.filter(email=user_info[0]).first()
    else:
        authorize_check = 'main/base.html'

    return render(request, 'main/contacts.html', {'authorize_check': authorize_check, 'avatar': acc.img})


def profile(request):
    user_info = request.session.get('user_info', [])
    if not user_info:
        return redirect(reverse('login_view'))

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')

        user_profile = Users.objects.filter(email=user_info[0]).first() or Businesses.objects.filter(
            email=user_info[0]).first()

        if user_profile:
            if email and not (
                    Users.objects.filter(email=email).exists() or Businesses.objects.filter(email=email).exists()):
                user_profile.email = email
                user_info[0] = email
                request.session['user_info'] = user_info
            if phone and not (Users.objects.filter(phone_number=phone).exists() or Businesses.objects.filter(
                    phone_number=phone).exists()):
                user_profile.phone_number = phone
            if birthday:
                user_profile.date_of_birth = birthday
            if password:
                user_profile.password = password
            user_profile.save()

            if 'avatar' in request.FILES:
                if user_profile.img.name != 'upldfile/base_avatar.jpg':
                    old_avatar_path = os.path.join(settings.MEDIA_ROOT, user_profile.img.name)
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)

                avatar = request.FILES['avatar']
                fs = FileSystemStorage()
                filename = fs.save('upldfile/' + avatar.name, avatar)
                user_profile.img = 'upldfile/' + avatar.name
                user_profile.save()

    next_book, prev_book = None, None
    acc = Businesses.objects.filter(email=user_info[0]).first()
    if not acc:
        acc = Users.objects.filter(email=user_info[0]).first()
        name = f'{acc.first_name} {acc.last_name}'
        birthday = str(acc.date_of_birth)

        next_book = []
        nb = Bookings.objects.filter(date_start__gt=timezone.now()).values('id_coworking', 'date_start', 'price')
        for book in nb:
            next_book.append({'image': Images.objects.filter(id_coworking=book['id_coworking']).first(),
                              'address': 'Заглушка для адреса', 'key': book['id_coworking'],
                              'time_start': timezone.localtime(book['date_start']).strftime('%d.%m.%Y - %H:%M'),
                              'cowork_name': CoworkingSpaces.objects.filter(id=book['id_coworking']).values(
                                  'coworking_name').first()['coworking_name'], 'price': book['price']
                              })

        prev_book = []
        nb = Bookings.objects.filter(date_start__lt=timezone.now()).values('id_coworking', 'date_start')
        for book in nb:
            prev_book.append({'image': Images.objects.filter(id_coworking=book['id_coworking']).first(),
                              'address': 'Заглушка для адреса', 'key': book['id_coworking'],
                              'time_start': timezone.localtime(book['date_start']).strftime('%d.%m.%Y - %H:%M'),
                              'cowork_name': CoworkingSpaces.objects.filter(id=book['id_coworking']).values(
                                  'coworking_name').first()['coworking_name']
                              })

    else:
        birthday = None
        name = acc.company_name

    context = {'email': acc.email, 'phone': acc.phone_number, 'password': acc.password, 'name': name,
               'birthday': birthday, 'avatar': acc.img, 'next_book': next_book, 'prev_book': prev_book}

    if Businesses.objects.filter(email=user_info[0]).exists():
        return render(request, 'main/profile_business.html', context)
    return render(request, 'main/profile_user.html', context)


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
            request.session['user_info'] = [email]

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
            request.session['user_info'] = [email]
            return JsonResponse({'success': 'User created successfully'}, status=201)

    return render(request, 'main/registration.html')


def coworking(request, cowork_id):
    user_info = request.session.get('user_info', [])
    acc = None
    if user_info:
        authorize_check = 'main/base_logged_in.html'
        acc = Businesses.objects.filter(email=user_info[0]).first()
        if not acc:
            acc = Users.objects.filter(email=user_info[0]).first()
        if Businesses.objects.filter(email=user_info[0]).exists():
            pass
    else:
        authorize_check = 'main/base.html'

    spaces = Services.objects.filter(id_coworking=cowork_id)
    images = Images.objects.filter(id_coworking=cowork_id)
    cowk = CoworkingSpaces.objects.filter(id=cowork_id).first()

    print(acc.id, type(acc.id))
    print(cowk.id_company, type(cowk.id_company))
    context = {'authorize_check': authorize_check, 'spaces': spaces, 'big_img': images[0], 'small_img': images[1:],
               'description': cowk.description, 'name_coworking': cowk.coworking_name,
               'avatar': acc.img if acc else None}

    return render(request, 'main/temp_coworking.html', context)
