from django.urls import path
from .views import SpeechToTextView

urlpatterns = [
    path('speech-to-text/', SpeechToTextView.as_view(), name='speech-to-text'),
]