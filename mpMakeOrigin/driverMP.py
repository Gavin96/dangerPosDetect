#coding=utf-8
#cv version :3.3.0
from cv2 import *
import cv2 as cv;
import numpy as np
import math
import os
import time 

class MPGenerator:
#	def __init__(self, videoPth, saveDataFolder, saveImgFolder, isInterlaced):
	def __init__(self, videoPth, saveImgFolder, isInterlaced):

		''' 
		@para videoPth path of video
		@saveImgFolder img save path
		@isInterlaced should always be true in this scenario
		'''
		self.video = cv.VideoCapture(videoPth)
		self._isInterlaced = isInterlaced
		self._saveImgFolder = saveImgFolder + "/"

	def generate(self, y1, y2, fileName):
		'''
		this generate two files mainly, an image for viewing convieniently 
		@para y1 lower-bound
		@para y2 upper-bound
		@para fileName name of image without extension, eg."o0,o1,o2,o3"
		'''
		if y1 % 2 != 0: y1 += 1

		imgPth = self._saveImgFolder + fileName + ".png"
#		dataPth = self._saveDataFolder + fileName + ".npy"

		height = int(math.ceil(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
		width = int(math.ceil(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)))
		frameCount = int(math.ceil(self.video.get(cv2.CAP_PROP_FRAME_COUNT)))

		print ("height: " + str(height))
		print ("width: " + str(width))

		print("frame number: " + str(frameCount))

		print(fileName + ".png" + " is been making...")
		
		if self._isInterlaced:
			vert_condensed = np.zeros((2 * frameCount, width, 3))
		else:
			vert_condensed = np.zeros((frameCount, width, 3))
		vert_condensed = vert_condensed.astype(np.uint8)

			
		self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
		frame_counter = 0
		
		success, frame = self.video.read()


		if not self._isInterlaced:
			while success:
				cv.imwrite(os.path.join(frameOutputPath, str(frame_counter) + '.jpg'))
				for col in range(width):
					sum_b = 0
					sum_g = 0;
					sum_r = 0
					
					for row in range(y1, y2):
						sum_b+=frame[row,col][0];
						sum_g+=frame[row,col][1];
						sum_r+=frame[row,col][2];
	
					b = sum_b / (y2-y1);
					g = sum_g / (y2-y1);
					r = sum_r / (y2-y1);
					
					value = np.array([b , g, r])
					vert_condensed[frame_counter, col, :] = value
 

				success, frame = self.video.read()
				frame_counter += 1
				print(frame_counter)
			np.save(dataPth, vert_condensed)	
			sp.imsave(imgPth, vert_condensed/255)
				
		else:			
			while success:
				for col in range(width):
#					e = o = np.zeros((1, 3))
					e_sum_b=0
					e_sum_g=0
					e_sum_r=0
					o_sum_b=0
					o_sum_g=0
					o_sum_r=0
					
					i, j = 0, 0
					for row in range(y1, y2, 2):
						e_sum_b += int(frame[row,col][0])
						e_sum_g += int(frame[row,col][1])
						e_sum_r += int(frame[row,col][2])
						i += 1
						
					for row in range(y1 + 1, y2 + 1, 2):
						j += 1
						o_sum_b+=int(frame[row,col][0])
						o_sum_g+=int(frame[row,col][1])
						o_sum_r+=int(frame[row,col][2])
						
					b = (e_sum_b) / i
					g = (e_sum_g) / i
					r = (e_sum_r) / i
					value = np.array([b, g, r])
					vert_condensed[frame_counter * 2, col, :] = value
					b = (o_sum_b) / j
					g = (o_sum_g) / j
					r = (o_sum_r) / j
					value = np.array([b, g, r])
					vert_condensed[(frame_counter*2)+1, col, :] = value
					
				frame_counter += 1
				# if frame_counter%10 == 0: print(frame_counter)
				success, frame = self.video.read()		
		cv.imwrite(imgPth, vert_condensed)

		print(fileName + ".png" + " is made successfully.")

root = 'D:/driverBodyDetect/sourceVideos/driverPart/'
outputPath = 'D:/driverBodyDetect/driverMotion2/driverMpOutput/'

range_map = {}

# 按照需求切分视频  1280*720  按照的是高度H的像素尺寸
# 卡车：  range_map[0]
range_map[0] = [160, 295, 430, 565, 700] #后续调整分割区域

for dirpath, dirnames, filenames in os.walk(root):
    for fileName in filenames:
    	if fileName[-4:] != ".avi":
    		continue 
    	# 制作存储MP的文件夹
    	oi = outputPath + fileName[0:-4] + "/"   
    	print ("\nthe output file is stored in:\n" + oi + '\n')
    	if not os.path.exists(oi):
    		os.mkdir(oi)

    	t = time.time()
    	mpGen = MPGenerator(os.path.join(dirpath, fileName), oi, True)

    	print("****** Begin processing video " + fileName + " ******\n")
    	t0 = time.time()
    	mpGen.generate(range_map[0][0], range_map[0][1], "o0") # up
    	t1 = time.time()
    	print("For producing o0.png of " + fileName + ", time spent: " +  str(t1 - t0) + "s.\n")

    	mpGen.generate(range_map[0][1], range_map[0][2], "o1") # mid
    	t2 = time.time()
    	print("For producing o1.png of " + fileName + ", time spent: " +  str(t2 - t1) + "s.\n")

    	mpGen.generate(range_map[0][2], range_map[0][3], "o2") # almost bottom
    	t3 = time.time()
    	print("For producing o2.png of " + fileName + ", time spent: " +  str(t3 - t2) + "s.\n")
    	
    	mpGen.generate(range_map[0][3], range_map[0][4], "o3") # bottom
    	t4 = time.time()
    	print("For producing o3.png of " + fileName + ", time spent: " +  str(t4 - t3) + "s.\n")


    	print("****** " + fileName + " transfered into MP'process is completed, and Time spent in total is : " +  str(time.time() - t) + "s ******\n")	