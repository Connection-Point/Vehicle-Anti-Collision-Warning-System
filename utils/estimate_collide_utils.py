import numpy as np
import os
import sys
import tensorflow as tf
from imutils.video import VideoStream
import cv2
import imutils
import time
from imutils.video import FPS
from sklearn.metrics import pairwise
import copy
import pathlib
from collections import defaultdict
import pygame
import threading


colors = np.random.uniform(0, 255, size=(100, 3))
font = cv2.FONT_HERSHEY_SIMPLEX
pygame.init()
# Caution_Sound = "sound/Caution.WAV"
# csound = pygame.mixer.Sound(Caution_Sound)
# Warning_Sound = "sound/Warning.WAV"
# wsound = pygame.mixer.Sound(Warning_Sound)
csound = pygame.mixer.Sound("sound/editedCaution.WAV")
wsound = pygame.mixer.Sound("sound/editedWarning.WAV")


def estimate_collide(indexesCars , boxesCars , image_np , crash_count_frames):
	height , width , channel = image_np.shape
	vehicle_crash = 0
	max_curr_obj_area = 0
	centerX = centerY = 0
	details = [0 , 0 , 0 , 0]
	for j in indexesCars:
		print (j)
		i = j
		xmin, ymin, w, h = boxesCars[i]
		obj_area = w * h
		if obj_area > max_curr_obj_area:
			max_curr_obj_area = obj_area
			details = [ymin, xmin, ymin+h, xmin+w]


	# cv2.putText(image_np,str(max_curr_obj_area) ,(50,250), font, 1.2,(255,255,0),2,cv2.LINE_AA)

	centerX , centerY = (details[1] + details[3])/(2*width) , (details[0] + details[2])/(2*height)
	if max_curr_obj_area>40000:
		# if (centerX < 0.2 and details[2] > 0.9) or (0.3 <= centerX <= 0.7) or (centerX > 0.8 and details[2] > 0.9):
		if 0.27 <= centerX <= 0.73:
			vehicle_crash = 1
			crash_count_frames = 10


	if vehicle_crash == 0:
		crash_count_frames = crash_count_frames - 1


	elif crash_count_frames > 0:
		sound_played = False
		if max_curr_obj_area <= 70000:

			cv2.putText(image_np,"Caution You're Getting Closer" ,(340,40), font, 1.2,(0,255,255),2,cv2.LINE_AA)
			if not sound_played:
				# play the sound in a separate thread
				threading.Thread(target=csound.play).start()
				sound_played = True
			elif sound_played:
				# play the sound in a separate thread
				threading.Thread(target=csound.stop).start()
				sound_played = True
		elif max_curr_obj_area > 70000:
			cv2.putText(image_np,"Warning, Collision Might Imminent" ,(420,40), font, 1.2,(0,0,255),2,cv2.LINE_AA)
			if not sound_played:
				# play the sound in a separate thread
				threading.Thread(target=wsound.play).start()
				sound_played = True
			elif sound_played:
				# play the sound in a separate thread
				threading.Thread(target=wsound.stop).start()
				sound_played = True

	return image_np , crash_count_frames 







# a.mp4(25)   56    74  110
# b.mp4(24)  5  270   292  368    509
# c.mp4(24)   0  111    166  189(many cars, but not in range)   290    494
# d.mp4  2
