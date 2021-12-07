#!/usr/bin/env python3

from _typeshed import Self
import sqlite3

class Car:
    def __init__(self, id, model, make, colour, number_plate):
        self.id = id
        self.number_plate = number_plate
        self.model = model
        self.make = make
        self.colour = colour
        self.verified = False
        
    def verificationResult(self, flag):
        self.verified = flag