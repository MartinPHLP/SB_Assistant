from utils import *
from snowboy_detection import snowboydecoder


####### Main #######


if __name__ == "__main__":

	detector = snowboydecoder.HotwordDetector(SB_MODEL, sensitivity=0.9, audio_gain=1)
	detector.start(detected_callback)
