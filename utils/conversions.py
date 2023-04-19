import boto3
import pyaudio
import speech_recognition as sr
from playsound import playsound
from .keys_and_paths import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY_ACCESS


####### Setup #######


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
		r.adjust_for_ambient_noise(source, duration=0.5)
		audio = r.listen(source)
		print("audio in")

	try:
		text = r.recognize_google(audio, language='fr-FR')
		print("\nText : ", text, "\n")
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
		client: client used to do the convertion
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
