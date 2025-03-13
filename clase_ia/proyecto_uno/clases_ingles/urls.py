from django.contrib import admin
from django.urls import path
from .views import inicio
from .views import register
from .views import dialogo
from .views import translate_word

urlpatterns = [
    path('', inicio, name="inicio"),
    path('register/', register, name="register"),
    path('dialogo/', dialogo, name= "dialogo"),
    path('translate-word/', translate_word, name="translate_word")
]
