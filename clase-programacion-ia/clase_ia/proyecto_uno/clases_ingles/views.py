from django.shortcuts import render
from .forms import StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
import openai
from gtts import gTTS
from django.http import JsonResponse, HttpResponse, FileResponse
import io
from openai import OpenAIError
from translate import Translator

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
def inicio(request):
    return render(request, 'index.html')

def dialogo(request):
    dialog = """
    Hello! My name is Alex. Today, I want to talk about chess. Chess is a fun game. It has two players. 
    Each player has sixteen pieces. The pieces are white and black.

    There are different pieces: pawns, knights, bishops, rooks, a queen, and a king. The king is very important. 
    If you lose the king, you lose the game!

    Chess is a game of thinking. You move the pieces on the board. You need a plan. You need to think before you move. 
    Good players think a lot!

    I like chess because it is fun and interesting. My favorite piece is the queen. The queen is very strong. 
    She can move in many directions.

    Do you like chess? Let’s play a game!
    """
    return render(request, "dialog.html", {"dialog": dialog})


def translate_word(request):
    if request.method == "GET":
        word = request.GET.get("word", "")

        if not word:
            return JsonResponse({"error": "No word provided"}, status=400)

        # Genera la traducción y un ejemplo de uso
        prompt = f"Translate the word '{word}' to Spanish and provide an example sentence using it in English."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        result = response["choices"][0]["message"]["content"].strip().split("\n")
        translation = result[0] if result else "No translation found"
        example = result[1] if len(result) > 1 else "No example found"

        return JsonResponse({"word": word, "translation": translation, "example": example})

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

def generate_audio(request, word):
    tts = gTTS(word, lang='en')
    
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0) 
    
    response = HttpResponse(audio_buffer, content_type='audio/mpeg')
    response['Content-Disposition'] = f'inline; filename="{word[:10].replace(" ", "_")}.mp3"'
    
    return response

def get_word_info(request, word):
    try:
        clean_word = word.replace(" ", "").replace(".", "").lower()
        translator = Translator(from_lang='english', to_lang='spanish')

        prompt = f"Provide a unique and random example sentence with level A1 using the word '{word}' in context. response only example no more please"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an English language assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=30
        )
        example_sentence = response['choices'][0]['message']['content'].strip()

        # Devolver la información como JSON
        return JsonResponse({
            'word': clean_word,
            'translation': translator.translate(word),
            'example': example_sentence
        })
    except OpenAIError  as e:
        return JsonResponse({
            'word': clean_word,
            'translation': translator.translate(word),
            'example': "AI no disponible"
        })
