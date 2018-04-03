#! /usr/bin/env python 
#coding=utf-8
#原视频尺寸： 1280*1440
#cv V3.3.0
from cv2 import *
import cv2 as cv;
import numpy as np


root = 'C:/driverBodyDetect/sourceVideos/driverVideos/'
# processedRoute = 'D:/driverBodyDetect/sourceVideos/driverPart/'

for dirpath, dirnames, filenames in os.walk(root):
	for fileName in filenames:
		if fileName[-4:] != '.avi':
			continue
		print('******   '+fileName+' is in processing   ******')
		print(dirpath + fileName)
		videoCapture = cv.VideoCapture(dirpath  + fileName)   #readVideo
		#check if video open successfully
		if (videoCapture.isOpened()):
			print 'Open successfully.'
		else:
			print 'Open failed.'
		fps = videoCapture.get(cv.CAP_PROP_FPS)
		size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)/2))#（1280，720）
		print size
		videoWriter = cv2.VideoWriter('D:/driverBodyDetect/sourceVideos/driverPart/' + fileName[:-4] + '_driverPart.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)

		success,frame = videoCapture.read()

		while success:

			frame = frame[size[1]:2*size[1],0:size[0]]
			videoWriter.write(frame)
			success, frame = videoCapture.read()
		videoCapture.release()
		print ('******   '+fileName[:-4] + '_driverPart.avi made finished   ******\n\n')
