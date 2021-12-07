class Car:
   def __init__(self, model, make, colour, number_plate, prediction_score):
        self.model = model
        self.make = make
        self.colour = colour
        self.number_plate = number_plate
        self.prediction = prediction_score
        self.verified = False
