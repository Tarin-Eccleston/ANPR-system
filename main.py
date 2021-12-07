#!/usr/bin/env python3

import json
import time
import argparse
import os

# SQL
from sqlite3.dbapi2 import Cursor
import sqlite3

# CV and Image Processing
from pytesseract import Output
import pytesseract
import imutils
import cv2

# application processes images of vehicles in the examples folder and reads number plates

def main():
    cursor = createDataBase()
    i = 0

    while True:
        # collect image
        image = cv2.imread("/examples/" str(i) + ".png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        i = i + 1

        # Todo: dnn to detect car and model/make/colour

        # Todo: process image for license plate using morphological operations to 
        # reveal dark text on white background
    	rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
		blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
		cv2.imshow("Blackhat", blackhat)

		# next, find regions in the image that are light
		squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
		light = cv2.threshold(light, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		cv2.imshow("Light Regions", light)

        # compute the Scharr gradient representation of the blackhat
		# image in the x-direction and then scale the result back to
		# the range [0, 255]
		gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,
			dx=1, dy=0, ksize=-1)
		gradX = np.absolute(gradX)
		(minVal, maxVal) = (np.min(gradX), np.max(gradX))
		gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
		gradX = gradX.astype("uint8")
		cv2.imshow("Scharr", gradX)

		# blur the gradient representation, applying a closing
		# operation, and threshold the image using Otsu's method
		gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
		gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
		thresh = cv2.threshold(gradX, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		cv2.imshow("Grad Thresh", thresh)

		# perform a series of erosions and dilations to clean up the
		# thresholded image
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)
		cv2.imshow("Grad Erode/Dilate", thresh)

		# take the bitwise AND between the threshold result and the
		# light regions of the image
		thresh = cv2.bitwise_and(thresh, thresh, mask=light)
		thresh = cv2.dilate(thresh, None, iterations=2)
		thresh = cv2.erode(thresh, None, iterations=1)
		cv2.imshow("Final", thresh, waitKey=True)

		# find contours in the thresholded image and sort them by
		# their size in descending order, keeping only the largest
		# ones
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]

        # put into OCR

        # Todo: verify plate with model/make

        # Todo: append to databese

def createDataBase():
    # define connection and cursor
    connection = sqlite3.connect('vehicle.db')
    cursor = connection.cursor()

    # create stores tables
    command = """CREATE TABLE IF NOT EXISTS
    vehicles(plate_id INTEGER PRIMARY KEY, number_plate TEXT, make TEXT, model TEXT)"""
    cursor.execute(command)

    return cursor

def appendVehicle(cursor, number_plate, model , make, colour, prediction score):

    # append next verified vehicle into SQLite database
    cursor.execute("INSERT INTO vehicle VALUES(NULL, ?, ?, ?, ?)", (vehicle.number_plate, vehicle.make, vehicle.model, vehicle.colour))

    # print results
    cursor.execute("SELECT * FROM vehicles")
    results = cursor.fetchall()

    return results

if __name__ == "__main__":
    main()


        
        