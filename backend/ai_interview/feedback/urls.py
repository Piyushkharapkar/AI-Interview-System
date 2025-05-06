from django.urls import path
from .views import evaluate_answers

urlpatterns = [
    path('evaluate/', evaluate_answers , name='evaluate_answer'),
]
