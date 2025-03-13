from django.contrib import admin
from django.urls import path
from .views import inicio
from .views import register
from .views import dialogo
from .views import translate_word
from .views import generate_audio
from .views import get_word_info

urlpatterns = [
    path('', inicio, name="inicio"),
    path('register/', register, name="register"),
    path('dialogo/', dialogo, name="dialogo"),
    path("translate-word/", translate_word, name="translate_word"),
    path('api/generate-audio/<str:word>/', generate_audio, name='generate_audio'),
    path('api/word-info/<str:word>/', get_word_info, name='word-info'),
]
