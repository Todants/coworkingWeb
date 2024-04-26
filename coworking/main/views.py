from django.shortcuts import render


def index(request):
    if request.POST:
        post_data = request.POST
        for key, value in post_data.items():
            print(f"{key}: {value}")
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
