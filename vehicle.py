#!/usr/bin/env python3

from _typeshed import Self
import sqlite3

class Car:
    def __init__(self, model, make, colour, number_plate, prediction_score):
        self.number_plate = number_plate
        self.model = model
        self.make = make
        self.colour = colour
        self.verified = False
        
    def verificationResult(self, flag):
        self.verified = flag