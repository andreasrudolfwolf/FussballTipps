from django.urls import path
from . import views

urlpatterns = [
    path('', views.startSeite, name='startSeite'),
    path('paarungen/', views.paarungen, name='paarungen'),
    path('tippen/', views.tippen, name='tippen'),
    path('loginSeite/', views.loginSeite, name='loginSeite'),
    path('registerSeite/', views.registerSeite, name='registerSeite')
]