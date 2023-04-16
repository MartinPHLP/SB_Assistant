import os
import time
import boto3
import openai
import random
import pyaudio
import snowboydecoder
import speech_recognition as sr
from playsound import playsound


polly_client = boto3.client(
	'polly',
	aws_access_key_id = str(os.getenv('AWS_ACCESS_KEY_ID')),
	aws_secret_access_key = str(os.getenv('AWS_SECRET_KEY_ACCESS')),
	region_name='eu-west-3'
)


openai.organization = str(os.getenv('OAI_ORGANIZATION_ID'))
openai.api_key = str(os.getenv('OAI_SECRET_KEY_ACCESS'))


# Chemin vers le modèle de détection de mot-clé Snowboy
model = 'resources/models/snowboy.umdl'

def text_to_speech(text, lang, filename):
	response = polly_client.synthesize_speech(Text=text,
	OutputFormat='mp3',
	VoiceId='Mathieu',
	LanguageCode=lang)

	# Enregistrez la réponse audio dans un fichier
	audio_file = open('output.mp3', 'wb')
	audio_file.write(response['AudioStream'].read())
	audio_file.close()

def detected_callback():

	audio_response1 = "Ouai gros ?"
	audio_response2 = "Tu veux quoi mon sauce ?"
	audio_response3 = "Ouai le zingue ?"
	audio_response4 = "Ouai ouai ouai ?"

	text_to_speech(random.choice([audio_response1, audio_response2, audio_response3]), "fr-FR", "output.mp3")
	playsound("output.mp3")
	text = listen_text()

	if text != 0:
		text_to_speech(response_of_ai(text), "fr-FR", "output.mp3")
		playsound("output.mp3")

def listen_text():

	r = sr.Recognizer()

	with sr.Microphone() as source:
		playsound("start.mp3")
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)
		print("ok")
		start_time = time.perf_counter()

	# Détection de l'endpoint
	try:
		text = r.recognize_google(audio, language='fr-FR')
		end_time = time.perf_counter()
		print(f"text understanded, time for understanding : {round(end_time - start_time, 2)} seconds")

		print("\n\n\n", text, "\n\n\n")
		return text

	except sr.UnknownValueError:
		audio_response1 = "Deso frero j'ai rien capté."
		audio_response2 = "Man, je comprends rien a ce que tu racontes."
		audio_response3 = "Frandjo tu racontes quoi ? Je pige pas."

		text_to_speech(random.choice([audio_response1, audio_response2, audio_response3]), "fr-FR", "output.mp3")
		playsound("output.mp3")
		return 0

	except sr.RequestError as e:
		print("Impossible d'obtenir les résultats de Google Speech Recognition ; {0}".format(e))
		return 0

def response_of_ai(input):

	start = time.perf_counter()
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "Tu es un assistant vocal. Tu te comportes comme un jeune de cite de 20 ans extremement vulgaire et agressif"},
			{"role": "user", "content": f"{input}"}
		],
		max_tokens=200,
		temperature=0.9
	)
	end = time.perf_counter()
	print(f"time for ia response : {round(end - start, 2)} seconds")
	return (completion['choices'][0]['message']['content'])


detector = snowboydecoder.HotwordDetector(model, sensitivity=0.9, audio_gain=1)
detector.start(detected_callback)
