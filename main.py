#!/usr/bin/env python3

import json
import time
import argparse
import os

# SQL
from sqlite3.dbapi2 import Cursor
import sqlite3

# CV and Image Processing
from skimage.segmentation import clear_border
import pytesseract
import numpy as np
import imutils
import cv2

# application processes images of vehicles in the examples folder and reads number plates


def main():
    cursor = createDataBase()
    i = 1

    while True:
        # collect image
        image = cv2.imread("examples/" + str(i) + ".jpg")
        cv2.imshow("image", image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        i = i + 1

        # Todo: dnn to detect car and model/make/colour

        # Todo: process image for license plate using deep learning

        # Todo: put into OCR

        # Todo: verify plate with model/make

        # Todo: append to databese

        while True:
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        cv2.destroyAllWindows()

        if i == 7:
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


def appendVehicle(cursor, number_plate, model, make, colour, country):

    # append next verified vehicle into SQLite database
    cursor.execute("INSERT INTO vehicle VALUES(NULL, ?, ?, ?, ?, ?)",
                   (vehicle.number_plate, vehicle.make, vehicle.model, vehicle.colour, vehicle.country))

    # print results
    cursor.execute("SELECT * FROM vehicles")
    results = cursor.fetchall()

    return results


if __name__ == "__main__":
    main()
