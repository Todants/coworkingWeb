from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view, name='login_view'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('profile', views.profile, name='profile'),
    path('book', views.temp, name='book'),
    path('coworking/<int:cowork_id>', views.coworking),
    path('registration', views.registration, name='registration'),

]
