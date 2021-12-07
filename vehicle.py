#!/usr/bin/env python3

from _typeshed import Self
import sqlite3
from sqlite3.dbapi2 import register_adapter

class Car:
    def __init__(self, id, number_plate, model, make, colour, country):
        self.id = id
        self.number_plate = number_plate
        self.model = model
        self.make = make
        self.colour = colour
        self.country = country
        self.verified = False
        
    def verificationResult(self, flag):
        self.verified = flag