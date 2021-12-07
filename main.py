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
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        i = i + 1

        # Todo: dnn to detect car and model/make/colour

        # image process
    	rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
		blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
		self.debug_imshow("Blackhat", blackhat)

        # put into OCR
        vehicle = vehicle(i, '', '', '', '')

        # Todo: verify plate with model/make

        # Todo: append to databese

        if i > 7:
            break

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


        
        