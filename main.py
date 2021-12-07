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
        image = cv2.imread(i + ".png")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        i = i + 1

        # dnn to detect car and model/make/colour

        # image process

        # put into OCR

        # verify plate with model/make

        # append to databese

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


        
        