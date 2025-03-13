from django.shortcuts import render
from .forms import StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import openai
from django.http import JsonResponse




def inicio(request):
    return render(request, 'index.html')


def translate_word(request):
    if request.method == "GET":
        word = request.GET.get("word","")
        
        prompt = f"Translate the la word '{word}' to Spanish and privide an example sentence using it in English."
        
        reponse =  openai.ChatCompletion.create(
            model= "gpt-3.5-turbo",
            messages=[{"role":"system", "content":prompt}]
        )
        
        
        result = reponse["choices"][0]["message"]["content"]
        return JsonResponse({"resultado": result })
        

def dialogo(request):
    dialogo = """
    Hello! My name is Tom. I like cars. I love fast cars. My favorite cars are sports cars.

Sports cars are very fast. They have big engines. They make a loud sound. Vroom!

My dream car is a red Ferrari. It is beautiful and very fast. It has two seats. It has big wheels. I want to drive a Ferrari one day.

Sports cars are expensive. But they are very cool! Do you like sports cars too?
    """
    
    return render(request,"dialog.html", {"texto": dialogo })

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        
        print(user_form.errors)
        print(student_form.errors)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            student =  student_form.save(commit=False)
            student.crated_by = user
            student.save()
            print("Entro el registro")
            #hacemos login()
            messages.success(request, 'Te has registrado con exito')
    else:
        user_form = UserCreationForm()
        student_form = StudentForm()
            
    return render(request,'register.html', {'user_form': user_form, 'student_form': student_form})
