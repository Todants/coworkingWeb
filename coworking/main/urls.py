from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view, name='login'),
    path('about', views.about),
    path('contacts', views.contacts),
    path('profile', views.profile),
    path('book', views.temp),
    path('coworking', views.coworking),
    path('registration', views.registration, name='registration'),

]
