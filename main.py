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
import cv2
from matplotlib import pyplot as plt

# deep learning
import tensorflow as tf
import object_detection
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

# application processes images of vehicles in the examples folder and reads number plates

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-3')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def main():
    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
    cursor = createDataBase()
    i = 1
    plates = []

    while True:
        # collect image
        image = cv2.imread("examples/" + str(i) + ".jpg")
        image_np = np.array(image)

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        i = i + 1

        # Todo: dnn to detect car and model/make/colour

        # Todo: process image for license plate using deep learning
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,
                    min_score_thresh=.8,
                    agnostic_mode=False)

        plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
        plt.show()

        # Todo: put into OCR
        options = "--psm 7 -c tessedit_char_whitelist=0123456789"
        text = pytesseract.image_to_string(roi, config=options)

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
