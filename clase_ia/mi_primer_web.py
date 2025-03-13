import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

openai.api_key = "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"

def conect_ia():
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "actua como un doctor experimentado que enseña sobre medicamentos"},
            {"role": "user", "content": "Recomiendame un medicamento para el dolor de cabeza"}
        ]
    )
    
    respuesta = response["choices"][0]["message"]["content"].strip()
    return respuesta
    

@app.route("/")
def home():
    saludo = conect_ia()
    return f"<h1>{saludo}</h1>"

if __name__ == "__main__":
    app.run(debug=True)