import serial


class Comunication(object):

    def __init__(self):
        self.comunication_serial = serial.Serial(0)

    def insert_water(self):
        self.comunication_serial.write("insert_water")

    def get_filled_pot(self):
        filled_pot = self.comunication_serial.readline()
        if filled_pot == "reached":
            self.stop_water()
        else:
            pass

    def stop_water(self):
        self.comunication_serial.write("stop_water")
