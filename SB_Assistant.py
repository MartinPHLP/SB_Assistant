import os
import time
import boto3
import openai
import random
import pyaudio
import speech_recognition as sr
from playsound import playsound
import audio.assistant_interactions as itrc
from snowboy_detection import snowboydecoder


####### Setup #######


openai.organization = str(os.getenv('OAI_ORGANIZATION_ID'))
openai.api_key = str(os.getenv('OAI_SECRET_KEY_ACCESS'))

AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
AWS_SECRET_KEY_ACCESS = str(os.getenv('AWS_SECRET_KEY_ACCESS'))

SB_MODEL = 'snowboy_detection/resources/models/snowboy.umdl'

polly_client = boto3.client(
	'polly',
	aws_access_key_id=AWS_ACCESS_KEY_ID,
	aws_secret_access_key=AWS_SECRET_KEY_ACCESS,
	region_name='eu-west-3'
)


####### Conversion functions ########


def speech_to_text():
	"""
	This function convert audio from mic to text.
	The recording is activate by hotword detection with snowboy engine.

	Args:
		none

	Returns:
		str: text in the audio if it's clear
		1: audio not clear
		0: else
	"""

	r = sr.Recognizer()

	with sr.Microphone() as source:
		playsound("./audio/start.mp3")

		# Adjust duration to have better results #
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)

		print("ok")
		start_time = time.perf_counter()

	try:
		text = r.recognize_google(audio, language='fr-FR')
		end_time = time.perf_counter()
		print(f"text understanded, time for understanding : {round(end_time - start_time, 2)} seconds\ntext : {text}")
		return text

	except sr.UnknownValueError:
		return 1

	except sr.RequestError as e:
		print("Impossible d'obtenir les résultats de Google Speech Recognition ; {0}".format(e))
		return 0


def text_to_speech(text, filename):
	"""
	This function convert text to audio.
	It use Polly model from AWS to convert the text to an .mp3 file.

	Args:
		text (str): text to read
		filename (str) : name of the file to read

	Returns:
		none
	"""

	result = polly_client.synthesize_speech(
		Text=text,
		OutputFormat='mp3',
		VoiceId='Mathieu',
		LanguageCode='fr-FR'
	)
	audio_file = open('./audio/output.mp3', 'wb')
	audio_file.write(result['AudioStream'].read())
	audio_file.close()


####### AI processing #######


def result_of_ai(input):
	"""
	This function use OpenAI API to treat the converted-to-text audio.

	Args:
		input (str): text from the conversion

	Returns:
		str: answer of the AI model
	"""

	start = time.perf_counter()
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "Tu es un assistant vocal. Tu te comportes comme un jeune" \
											"de cite de 20 ans extremement vulgaire et agressif"},
			{"role": "user", "content": f"{input}"}
		],
		max_tokens=200,
		temperature=0.9
	)
	end = time.perf_counter()
	print(f"time for ia result : {round(end - start, 2)} seconds")
	return (completion['choices'][0]['message']['content'])


####### Callback function #######


def detected_callback():
	"""
	This function is called when the hotword is detected.
	It asks for user demand, convert the audio demand to text,
	treat the demand with AI model, and play the answer with
	polly model.
	Exit if google recognition fail.

	Args:
		none

	Returns:
		none
	"""

	text_to_speech(random.choice(itrc.ask), "./audio/output.mp3")
	playsound("./audio/output.mp3")
	text = speech_to_text()
	if type(text) == str:
		text_to_speech(result_of_ai(text), "./audio/output.mp3")
		playsound("./audio/output.mp3")
	elif text == 1:
		text_to_speech(random.choice(itrc.unclear), "./audio/output.mp3")
		playsound("./audio/output.mp3")
	elif text == 0:
		for i in range(3):
			playsound("./audio/start.mp3")
			time.sleep(0.3)
		exit()


####### Main #######


if __name__ == "__main__":

	detector = snowboydecoder.HotwordDetector(SB_MODEL, sensitivity=0.9, audio_gain=1)
	detector.start(detected_callback)
