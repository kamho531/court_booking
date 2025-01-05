from django.urls import path
from . import views

urlpatterns = [
    #path('', views.custom_login, name='custom_login'),
    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_success/', views.update_success, name='update_success'),
    path('userlogout/', views.custom_logout, name='custom_logout'),
    path('logout_success/', views.logout_success, name='logout_success'),

]
