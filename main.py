from flask import Flask, render_template, request, send_file
from gtts import gTTS
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key='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')

def correct_text_with_gpt4(text):
    """Corrige le texte avec GPT-4 pour les erreurs d'orthographe et de grammaire."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Vous êtes un correcteur de texte."},
            {"role": "user", "content": f"Corrige le texte suivant pour les fautes d'orthographe et de grammaire en conservant la langue originale :\n\n{text}"}
        ],
        max_tokens=150,
        temperature=0.5
    )
    corrected_text = response.choices[0].message.content.strip()
    return corrected_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        language = request.form['language']
        name = request.form['name']

        corrected_text = correct_text_with_gpt4(text)

        # Langues supportées par gTTS
        lang_dict = {
            "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali", "bs": "Bosnian",
            "ca": "Catalan", "cs": "Czech", "cy": "Welsh", "da": "Danish", "de": "German",
            "el": "Greek", "en": "English", "eo": "Esperanto", "es": "Spanish", "et": "Estonian",
            "fi": "Finnish", "fr": "French", "gu": "Gujarati", "hi": "Hindi", "hr": "Croatian",
            "hu": "Hungarian", "hy": "Armenian", "id": "Indonesian", "is": "Icelandic", "it": "Italian",
            "ja": "Japanese", "jw": "Javanese", "km": "Khmer", "kn": "Kannada", "ko": "Korean",
            "la": "Latin", "lv": "Latvian", "mk": "Macedonian", "ml": "Malayalam", "mr": "Marathi",
            "my": "Burmese", "ne": "Nepali", "nl": "Dutch", "no": "Norwegian", "pl": "Polish",
            "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "si": "Sinhala", "sk": "Slovak",
            "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili",
            "ta": "Tamil", "te": "Telugu", "th": "Thai", "tl": "Filipino", "tr": "Turkish",
            "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese", "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)", "zh": "Mandarin"
        }

        language = language.lower()
        if language in lang_dict:
            filename = f"{name}.mp3"
            gTTS(corrected_text, lang=language).save(filename)
            return send_file(filename, as_attachment=True)
        else:
            return "Language not supported.", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
