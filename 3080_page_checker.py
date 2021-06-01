from requests_html import HTMLSession
from time import sleep
import os
from twilio.rest import Client
from random import randint
from random import random
import mega_ip_rotator
import keyboard
# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm

import pytesseract

# importing OpenCV
import cv2

from PIL import ImageGrab

import pynput
import mouse

from pprint import pprint
from datetime import datetime


mousecont = pynput.mouse.Controller()
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'




def make_call(number,message):
		# Download the helper library from https://www.twilio.com/docs/python/install
	#import os
	#from twilio.rest import Client


	# Your Account Sid and Auth Token from twilio.com/console
	# and set the environment variables. See http://twil.io/secure
	account_sid = 'AC08936d34c6ef76531479429571b357b7'
	auth_token = 'f204148232298e73b4fdbe65aaaf7a0a'
	client = Client(account_sid, auth_token)

	call = client.calls.create(
							twiml='<Response><Say>' + message +'</Say></Response>',
							to=number,
							from_='+19512929092'
						)

	print(call.sid)

def check_page_for_string(url,string):

	#create the session
	session = HTMLSession()

	#define our URL
	#url = 'https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816'

	#use the session to get the data
	r = session.get(url)

	#Render the page, up the number on scrolldown to page down multiple times on a page
	#r.html.render(sleep=1, keep_page=True, scrolldown=1)
	r.html.render(retries = 8, wait = random()*3, scrolldown=randint(1,5), sleep = randint(1,2), reload = True, timeout = 8.0, keep_page = False)

	# now we have a string containing all text on the webpage
	text = r.html.text
	# return text
	if text.find(string) < 0:
		#print('the text isnt there!')
		return 'not found'
	else:
		#print('the text is still there')
		return 'found'



#print(check_page_for_string('https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816','unleashes new gaming possibilities'))
#make_call('6196395379','playstation 5 disk edition page has changed. Are you feeling it now Mr. Crabs?')


def real_click_fixed():
    '''This function clicks the mouse with realistic errors:
        occasional accidental right click (not any more)
        occasional double click
        occasional no click
    '''
    if randint(1, 19) != 1:
        sleep(93 / randint(83,201))
        pyautogui.click()
    else:
        tmp_rand = randint(1, 3)
        if tmp_rand == 1:
            #double click
            pyautogui.click()
            sleep(randint(43, 113) / 1000)
            pyautogui.click()
        elif tmp_rand == 2:
            pyautogui.click(button = 'left')

def dumpclean(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k)
                dumpclean(v)
            else:
                print('%s : %s' % (k, v))
    elif isinstance(obj, list):
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print(v)
    else:
        print(obj)

def draw_boxes(img):
	# from pytesseract import Output
	# img = load_screenshot()


	d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	n_boxes = len(d['level'])
	# print(dir(n_boxes))
	# print(type(d))
	# pprint(dir(d))
	for i in range(n_boxes):
	    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('img', img)
	cv2.waitKey(0)

def take_new_screenshot():
		img = nm.array(ImageGrab.grab())
		cv2.imwrite('screenshot.png', img)

def load_screenshot():
	return cv2.imread('screenshot.png')

# def screen_get():
# 	img = nm.array(ImageGrab.grab())
# 	# cv2.imwrite('screenshot.png', img)
# 	return img

def image_data_return(img):
	d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	return d

def search_image_for_substring(substring,img_dict):
	#takes in substring and image_to_data image dictionary, returns index as int
	list = img_dict['text']
	lower_list = [each_string.lower() for each_string in list]
	# print(lower_list)
	sub = substring.lower()
	index_list = [s for s in lower_list if sub in s]
	return lower_list.index(index_list[0])

def text_coords(index,img_dict):
	d = img_dict
	i = index
	(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	coords = [x+w/2,y+h/2]
	return coords

def move_mouse_and_click(coords):
	# mousecont.position = (coords[0], coords[1])
	currentpos = mousecont.position
	# print(type(currentpos))
	# print(currentpos)
	mouse.move(mouse.mouse_bez(currentpos, coords, deviation=10, speed=randint(1,2)))

	# sleep(1)
	# mousecont.click(pynput.mouse.Button.left, 1)
	mouse.real_click_fixed()

def imToString(img):

    # Path of tesseract executable
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    # while(True):

    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.
    # cap = ImageGrab.grab(bbox =(700, 300, 1400, 900))
    # cap = ImageGrab.grab()
    # cap = ImageGrab.grab(xdisplay=109051911)
    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(
            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
            lang ='eng')
    # print(tesstr)
    return tesstr

def move_and_click_word(word):
	sleep(1)
	take_new_screenshot()
	# sleep(3)
	d = image_data_return(load_screenshot())
	move_mouse_and_click(text_coords(search_image_for_substring(word,d),d))


def check_page():

	decrement = 10
	robot = 0
	# mega_ip_rotator.download_US_server_dict()

	while decrement > 0:
		sleep(randint(5,10))


		try:
			while True:
				move_and_click_word('robot')
				print('clicked robot')
				robot = 1
				sleep(0.7)
				mouse.move(mouse.mouse_bez(mousecont.position, (100,100), deviation=10, speed=randint(1,2)))

			# sleep(randint(3,4)) #wait for page load

		except:
			print('did not find word robot')
			robot = 0
		# mousecont.click(pynput.mouse.Button.left, 1)
			# sleep(0.5)
			keyboard.press_and_release('f5')
			print('pressed f5')
		print(datetime.now())

		sleep(randint(3,4)) #wait for page load
		# mousecont
		if randint(0,1):
			scroll_amount = randint(1,5)
			mousecont.scroll(0, -scroll_amount)
			sleep(randint(1,2))
			mousecont.scroll(0, scroll_amount+2)


		print('capturing image')
		take_new_screenshot()
		string_from_screen = imToString(load_screenshot())
		print(string_from_screen)
		# string_from_screen.lower().find('when you reach the front')
		# print(string_from_screen)

		# if string_from_screen.find('unleashes new gaming possibilities') > -1
		if string_from_screen.lower().find('Delivered') > -1:
		# if string_from_screen.lower().find('unleashes new') > -1:
			print('found')
			print('calling...')
			sleep(5)
			make_call('6196395379','3080 page has changed. Are you feeling it now Mr. Crabs?')
			sleep(1)
			make_call('6193238545','3080 page has changed. Are you feeling it now Mr. Crabs?')
			sleep(5)
			exit()
		else:
			print('not found')

check_page()
# sleep(2)
# cv2.imwrite('screenshot.png', screen_get())
# boxes_get()
# exit()
