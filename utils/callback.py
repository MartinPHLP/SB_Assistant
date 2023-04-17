import time
import random
from .conversions import *
from .ai_processing import *
import audio.assistant_interactions as itrc


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
