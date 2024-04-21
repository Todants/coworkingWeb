from django.shortcuts import render


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
