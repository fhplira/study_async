from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('log_in/', views.log_in, name='login'),
    path('logout/', views.logout, name='logout'),

]
