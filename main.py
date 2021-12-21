#!/usr/bin/env python3

import json
import time
import argparse
import os

# SQL
from sqlite3.dbapi2 import Cursor
import sqlite3

# CV and Image Processing
import pytesseract
import numpy as np
from numpy.lib.type_check import imag
import imutils
import glob
import cv2
from matplotlib import pyplot as plt

# deep learning
import tensorflow as tf
import object_detection
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util


def main():
    cursor = createDataBase()
    i = 1
    plates = []

    for imagePath in glob.glob("examples" + "/*.jpg"):
        # collect image
        image = cv2.imread(imagePath)
        image_np = np.array(image)

        i = i + 1

        # Todo: dnn to detect car and model/make/colour

        # Todo: process image for license plate using deep learning

        # Todo: put into OCR
        # options = "--psm 7 -c tessedit_char_whitelist=0123456789"
        # text = pytesseract.image_to_string(roi, config=options)

        # Todo: verify plate with model/make
        # API_KEY = ???
        # Account_Key = ???

        # send request with license plate number
        # response = requests.get('https://test.carjam.co.nz/a/report:create?key={API_KEY}&account_key={Account_Key}&basic=1&plate={plateNumber}')

        # polling every 100 ms to check if report is ready
        # while response.completed != true
        #     sleep(0.1)

        # retrieve results
        # result = requests.get('https://test.carjam.co.nz/a/report:get&ref={response.ref}')

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
