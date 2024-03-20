from django.urls import path
from . import views

urlpatterns = [
    path('', views.startSeite, name='startSeite'),
    path('paarungen/', views.paarungen, name='paarungen'),
    path('gruppenspiele/<int:id>/', views.gruppenspiele, name='gruppenspiele'),
    path('tippen/', views.tippen, name='tippen'),
    path('tippen_eingabe/<int:id>/', views.tippen_eingabe, name='tippen_eingabe'),
    path('loginSeite/', views.loginSeite, name='loginSeite'),
    path('logoutSeite/', views.logoutSeite, name='logoutSeite'),
    path('registerSeite/', views.registerSeite, name='registerSeite')
]