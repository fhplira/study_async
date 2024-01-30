from django.urls import path
from . import views

urlpatterns = [
    path('add_course_pack', views.add_course_pack, name='add_course_pack'),
    path('course_pack/<int:id>', views.course_pack, name='course_pack'),
]
