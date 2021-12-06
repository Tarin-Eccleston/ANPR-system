#!/usr/bin/env python3

import base64
import json
import os
import ssl
import http.client as httplib
import time
import sqlite3

def sightHoundAPI():

    # initialise and setup authorisation for SightHound API
    headers = {"Content-type": "application/json",
    "X-Access-Token": "8R6JQJ9YhG89sTD6qvW49i2rpCmf91Rrxz9r"}
    conn = httplib.HTTPSConnection("dev.sighthoundapi.com",
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))

    # send data from file (can select between 1.jpg and 7.jpg)
    image_data = base64.b64encode(open('exportMin/6.jpg', "rb").read()).decode()

    params = json.dumps({"image": image_data})

    # send request and retrieve response
    # start processing timer
    tic = time.clock()
    conn.request("POST", "/v1/recognition?objectType=licenseplate", params, headers)
    response = conn.getresponse()
    result = response.read()

    # finish processing timer
    toc = time.clock()
    processingTime = round(toc - tic,4)

    # create Python dictionary from results
    dictResult = json.loads(result)

    return processingTime,dictResult

def process(dictResult):

    # find highest confidence value
    confidenceValueList = []
    for i in dictResult['objects']:
        confidenceValueList.append(i['licenseplateAnnotation']['attributes']['system']['string']['confidence'])

    # if no license plates are detected
    if not confidenceValueList:
        plateNumber = "NULL"
        confidenceValue = 0.0 
    
        return plateNumber,confidenceValue

    confidenceValue = max(confidenceValueList)

    # find corresponding plate number to highest confidence value
    confidenceValueIndex = confidenceValueList.index(confidenceValue)
    plateNumber = dictResult['objects'][confidenceValueIndex]['licenseplateAnnotation']['attributes']['system']['string']['name']

    return plateNumber,confidenceValue

def createDataBase():

    # define connection and cursor
    connection = sqlite3.connect('licensePlate.db')
    cursor = connection.cursor()

    # create stores tables
    command = """CREATE TABLE IF NOT EXISTS
    plates(plate_id INTEGER PRIMARY KEY, licensePlate TEXT, confidenceValue REAL, processingTime REAL)"""
    cursor.execute(command)

    return cursor

def appendLicensePlate(cursor,plateNumber,confidenceValue,processingTime):

    # append next predicted number plate into SQLite database
    cursor.execute("INSERT INTO plates VALUES(NULL, ?, ?, ?)", (plateNumber, confidenceValue, processingTime))

    # print results
    cursor.execute("SELECT * FROM plates")
    results = cursor.fetchall()

    return results

def findLicensePlate(): 

    # P1.1 - P1.3
    processingTime,dictResult = sightHoundAPI()
    plateNumber,confidenceValue = process(dictResult)

    # 
    print("\nLicense Plate Prediction : " + plateNumber)
    print("Confidence : " + str(round(confidenceValue,4)))
    print("\nLicense Plate Processing time (Sighthound) : " + str(processingTime) + " seconds")

    # P1.4
    cursor = createDataBase()
    results = appendLicensePlate(cursor,plateNumber,confidenceValue,processingTime)

    print("\nSuccessfully appended data to SQLite database")
    print(results)
    print("")

    return plateNumber

if __name__ == "__main__":
    findLicensePlate()


        
        