#V1.01
''' This python script provides the functions to display simple scrolling text on
a Pimoroni Unicorn hat, and add-on board for the Raspberry Pi model B+'''

import unicornhat as UH 
from bitarray import bitarray
import time
#import letter definitions and mappings
from UHScroll_defs import *
from UHScroll_defs_lowercase import *

'''It assumes the Pi/hat will orientated with the long side of the Pi without any connectors on
the bottom, i.e. the Hat will be rotated 90 degrees clockwise (assuming the "UNICORN HAT" label and 
Pimoroni logo are normally at the bottom of the hat. If you want to use a different orientation  
then you can alter the UH.rotation value in the show_letter function below. You may also need to adjust or omit
the flip call which is used to ensure that the bitarray definitions in uhscroll_letters are the correct 
way round for easy reading'''

flip = [7,6,5,4,3,2,1,0]


def show_letter_rgb(letter,r,g,b): #displays a single letter on th UH
	UH.rotation(270)		
	for i in range(8):
		for j in range(8):
			if letter[j][i]:
				
				UH.set_pixel(j,flip[i],r,g,b)
				
					
			else:
				UH.set_pixel(j,flip[i],0,0,0)

	UH.show()


'''scrolling is achieved by redrawing the letter with a column of the bitarray shifted to the left and a new blank column
added to the right'''
def scroll_word_rgb(word,r,g,b,speed): # scrolls a word across the UH
	for s in range(len(word[0])):
		show_letter_rgb(word,r,g,b)
		time.sleep(speed)
		for i in range(8):
			word[i].pop(0)
			word[i].append(0)

def make_word(words): # takes a list of chars and concats into a word by making one big bitarray
	bigword = [bitarray(''),bitarray(''), bitarray(''),bitarray(''), bitarray(''),bitarray(''), bitarray(''),bitarray('')]
	for w in range(len(words)):
		for i in range(len(words[w])):
			bigword[i] = bigword[i] + words[w][i]
	return bigword
	
def trim_letter(letter): #trims a char's bitarray so that it can be joined without too big a gap
	trim = []
	for c in range(len(letter)):
		trim.append(letter[c].copy())
	if letter not in super_wides:
		for i in range(8):
			if letter not in wides:
				trim[i].pop(0)
			trim[i].pop(0)
			trim[i].pop(5)
			if letter in narrows:
				trim[i].pop(0)
			if letter in super_narrow:
				trim[i].pop(0)
				
	return trim

def map_character(chr):
	if chr in mapping:
		return mapping[chr]
	else:
		return mapping['_']



def map_character_lowercase(chr):
	if chr in mapping_lowercase:
		return mapping_lowercase[chr]
	else:
                return mapping_lowercase['_']




def load_message_uppercase_rgb(message):
	unicorn_message = []
	message = '  ' + message # pad the message with a couple of spaces so it starts on the right
	skip = 0
	for ch in (range(len(message))):
		#print message[ch]
		if skip != 0:
			skip-=1
		else:
			if message[ch] == '~':
				spec = message[ch+1] + message[ch+2] + message[ch+3] + message[ch+4] + message[ch+5]
				unicorn_message.append(trim_letter(map_character(spec)))
				skip = 5
			else:
				unicorn_message.append(trim_letter(map_character(message[ch].upper())))
		
	return(unicorn_message)


def load_message_lowercase_rgb(message):
	unicorn_message = []
	message = '  ' + message # pad the message with a couple of spaces so it starts on the right
	skip = 0
	for ch in (range(len(message))):
		#print message[ch]
		if skip != 0:
			skip-=1
		else:
			if message[ch] == '~':
				spec = message[ch+1] + message[ch+2] + message[ch+3] + message[ch+4] + message[ch+5]
				unicorn_message.append(trim_letter(map_character_lowercase(spec)))
				skip = 5
			else:
				unicorn_message.append(trim_letter(map_character_lowercase(message[ch])))
		
	return(unicorn_message)



def unicorn_scroll_uppercase_rgb(text,r,g,b,speed):
	#try:
	scroll_word_rgb(make_word(load_message_uppercase_rgb(text)),r,g,b,speed)
	#except: 
		#print 'Enter unicorn_scroll(message,colour,brightness,speed) where '
		#print 'message is a string, colour is either red,white,blue,green,pink, yellow, orange or cyan'
		#print 'brightness is a integer 0-255 and speed is the time between chars'
	
def unicorn_scroll_lowercase_rgb(text,r,g,b,speed):
	#try:
	scroll_word_rgb(make_word(load_message_lowercase_rgb(text)),r,g,b,speed)
	#except: 
		#print 'Enter unicorn_scroll(message,colour,brightness,speed) where '
		#print 'message is a string, colour is either red,white,blue,green,pink, yellow, orange or cyan'
		#print 'brightness is a integer 0-255 and speed is the time between chars'

