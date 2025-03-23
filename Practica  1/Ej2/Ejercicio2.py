import requests
from abc import ABC, abstractmethod
import json

HUGGING_FACE_API_KEY = "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"
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}


# Cargar el archivo JSON
with open('config.json', 'r') as file:
    config = json.load(file)

#Clase abstracta base
class LLM(ABC):
    @abstractmethod
    def generate_summary(self, text, input_lang, output_lang, model):
        pass

#Clase BasicLLM
class BasicLLM(LLM):
    def __init__(self, texto):
        self.texto = texto

    def generate_summary(self, text, input_lang, output_lang, model):
        payload = {"inputs": text}
        response = requests.post(f"{HUGGING_FACE_API_URL}{model}", headers=HEADERS, json=payload)
        return response.json()[0]["summary_text"] if response.status_code == 200 else "Error en la generación."

# Clase Decorator
class LLMDecorator(LLM):
    def __init__(self, wrapped):
        self.texto_decorado = wrapped
    @abstractmethod
    def generate_summary(self, text, input_lang, output_lang, model):
        pass

#Traslation decorador
class TranslationDecorator(LLMDecorator):
    def generate_summary(self, text, input_lang, output_lang, model):
        a_traducir = self.texto_decorado.generate_summary(text, input_lang, output_lang, model)
        payload = {"inputs": a_traducir}
        response = requests.post(f"{HUGGING_FACE_API_URL}{model_translation}", headers=HEADERS, json=payload)
        return response.json()[0]["translation_text"] if response.status_code == 200 else "Error en la traducción."
        

#Expansion decorador
class ExpansionDecorator(LLMDecorator):
    def generate_summary(self, text, input_lang, output_lang, model):
        a_generar = self.texto_decorado.generate_summary(text, input_lang, output_lang, model)
        payload = {
            "inputs": a_generar,
            "parameters": {
                "max_new_tokens": 200,
            }
        }
        response = requests.post(f"{HUGGING_FACE_API_URL}{model_expansion}", headers=HEADERS, json=payload)
        return response.json()[0]["generated_text"] if response.status_code == 200 else "Error en la expansión."


# Acceder a los datosP
texto = config['texto']
input_lang = config['input_lang']
output_lang = config['output_lang']
model_llm = config['model_llm']
model_translation = config['model_translation']
model_expansion = config['model_expansion']

if __name__ == "__main__":
    basic_llm = BasicLLM(texto)
    resumen = basic_llm.generate_summary(texto, input_lang, output_lang, model_llm)
    print("\nResumen básico:\n", resumen)

    translation_llm = TranslationDecorator(basic_llm)
    traduccion = translation_llm.generate_summary(texto, input_lang, output_lang, model_llm)
    print ("\nResumen traducido:\n", traduccion)

    
    expansion_llm = ExpansionDecorator(basic_llm)
    expansion = expansion_llm.generate_summary(texto, input_lang, output_lang, model_llm)
    print("\nResumen expandido:\n", expansion)


    expansion_llm = ExpansionDecorator(translation_llm)
    traduccion_expansion = expansion_llm.generate_summary(texto, input_lang, output_lang, model_llm)
    print("\nResumen traducido y expandido:\n", traduccion_expansion)



