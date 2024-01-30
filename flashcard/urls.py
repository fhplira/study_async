from django.urls import path
from . import views

urlpatterns = [
    path('new_flashcard/', views.new_flashcard, name='new_flashcard'),
    path('delete_flashcard/<int:id>/', views.delete_flashcard, name='delete_flashcard'),
    path('init_challenge/', views.init_challenge, name='init_challenge'),
    path('list_challenge/', views.list_challenge, name='list_challenge'),
    path('challenge/<int:id>/', views.challenge, name='challenge'),
    path('answer_flashcard/<int:id>/', views.answer_flashcard, name='answer_flashcard'),
    path('report/<int:id>/', views.report, name='report')
]
