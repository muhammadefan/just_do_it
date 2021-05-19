"""
Program Structure

Function 'record_audio': accepting and recording input data
Function 'respond': responding based on the command given
Function 'speak_audio': converting texted-response to be a voice data

additional package: 'pyaudio' (https://www.lfd.uci.edu/~gohlke/pythonlibs/#chebyfit)
search 'pyaudio', then pick the version which is compatible to your engine (OS version, python version)
"""

import speech_recognition as sr
import webbrowser # launching browser
import playsound
import os
import random

from gtts import gTTS # google Text-To-Speech
from time import ctime # current time


# initiate the name of engine (bot) & user
class name:
    def setName(self, *names):
        self.bot = 'kirin'
        self.person = 'efan'

# initiate variable to read the voice
r = sr.Recognizer()

# record the voice - speech-to-text
def record_audio(ask=False):
	with sr.Microphone() as source:
		if ask:
			speak_audio(ask)

		# read the voice
		audio = r.listen(source)
		voice_data = ''
		try:
			voice_data = r.recognize_google(audio) # speech-to-text

		# handling error if your voice is not recognizeable
		except sr.UnknownValueError:
			speak_audio('Sorry, can you repeat it again?')

		# handling error when google's server is having a problem
		except sr.RequestError:
			speak_audio('Sorry, there is problem on the server side')

		# print what user said
		print(f'>> {voice_data}')
	return voice_data


# input to the system
def respond(voice_data):
	# respond 1
	if input_option(['good morning','good afternoon','good evening','hi','hello','kirin','hey']):
		# initiate the time
		times = ctime()[11:13]
		times = int(times) # convert the datatype from string into integer

		# if the time showing 4-11 o'clock, respond with 'good morning'
		if times in range(4,12): 
			time='good morning'
		# if the time showing 12-19 o'clock, respond with 'good afternoon'
		elif times in range(12,20): 
			time='good afternoon'
		# if the time showing 20-24 & 1-3 o'clock, respond with 'good evening'
		elif times in range(20,25) or range(1,4): 
			time='good evening'

		# list of responds
		greetings = [f'{time}, how can i help you {name.person}', f'hey, how\'s life?', f'hi, i am {name.bot}, what do you want to do?']
		# randomly choose the responds
		greet = greetings[random.randint(0,len(greetings)-1)]
		speak_audio(greet)

	# respond 2
	elif input_option(['what is your name','who are you','what\'s your name']):
		speak_audio(f'i am {name.bot}')

	# respond 3
	elif 'what time is it' in voice_data:
		# read current time using 'ctime()'
		speak_audio(ctime())

	# respond 4
	elif 'search' in voice_data:
		# asking the name of someting that you want to search
		search = record_audio('what do you want to look for?')
		url = 'https://google.com/search?q=' + search
		# open the browser and do searching about something
		webbrowser.get().open(url)

		speak_audio(f'\nHere is what I found for {search}')

	# respond 5
	elif 'find location' in voice_data:
		# asking the name of location
		location = record_audio('where do you want to go?')
		url = 'https://google.nl/maps/place/' + location + '/&amp'
		# open the browser and google maps
		webbrowser.get().open(url)

		speak_audio(f'\nHere is the location of {location}')

	# respond 6
	elif input_option(['exit','bye','quit','see you']):
		speak_audio('see you later')
		exit()


# find the option
def input_option(sentences):
	for i in sentences:
		if i in voice_data:
			return True


# text-to-speech
def speak_audio(audio_string):
	# saving audio file
	rand = random.randint(1,1000)
	audio_file = 'audio_' + str(rand) + '.mp3'
	# text-to-speech
	tts = gTTS(text=audio_string, lang='en')
	tts.save(audio_file)
	# make it speaking
	playsound.playsound(audio_file)
	print(f'{name.bot}: {audio_string}')
	# deleting audio files
	os.remove(audio_file)


# run the class
name = name()

# run the function
print('Listening..\n')

while 1: # looping forever (1 == True / 0 == False)
	voice_data = record_audio() # record the input
	respond(voice_data) # respond to the input
