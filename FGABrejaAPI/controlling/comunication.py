import serial
import time


class Comunication(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Comunication, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.comunication_serial = serial.Serial('/dev/ttyACM0', 9600)

    # Pre Brewery Stage Serial Comunication
    def insert_water(self):
        self.comunication_serial.write("insert_water".encode())
        time.sleep(2)

    def get_pot_level(self):
        self.comunication_serial.write("check_level".encode())
        time.sleep(2)
        pot_level = self.comunication_serial.readline()
        print(pot_level)
        pot_level = pot_level.splitlines()
        return bool(pot_level[0])

    def stop_water(self):
        self.comunication_serial.write("stop_water".encode())
        time.sleep(2)

    # Brewery Stage Serial Comunication
    def turn_on_engine(self):
        self.comunication_serial.write("turn_on_engine".encode())
        time.sleep(2)

    def turn_off_engine(self):
        self.comunication_serial.write("turn_off_engine".encode())
        time.sleep(2)

    def turn_on_resistor(self, temperature=None):
        if temperature is not None:
            # self.turn_off_resistor(1)
            # time.sleep(2)
            message = "turn_on_resistor_1:%.2f" % temperature
            self.comunication_serial.write(message.encode())
        else:
            self.comunication_serial.write("turn_on_resistor_2".encode())
        time.sleep(2)

    # Boiling Stage Serial Comunication
    def add_hop(self, engine_id):
        message = "add_hop:%d" % engine_id
        self.comunication_serial.write(message.encode())
        time.sleep(2)

    def turn_off_resistor(self, pot):
        message = "turn_off_resistor_%d" % pot
        self.comunication_serial.write(message.encode())
        time.sleep(2)

    # Cooling Stage Serial Comunication
    def turn_on_chiller(self):
        self.comunication_serial.write("turn_on_chiller".encode())
        time.sleep(2)

    def turn_off_chiller(self):
        self.comunication_serial.write("turn_off_chiller".encode())
        time.sleep(2)

    # Fermentation Stage Serial Comunication
    def turn_on_freezer(self, temperature):
        message = "turn_on_freezer:%.2f" % temperature
        self.comunication_serial.write(message.encode())
        time.sleep(2)

    # Common Stages Serial Comunication
    def activate_alarm(self):
        self.comunication_serial.write("activate_alarm".encode())
        time.sleep(2)

    def read_thermal_sensor(self):
        self.comunication_serial.write("read_thermal_sensor".encode())
        time.sleep(2)
        temperature = self.comunication_serial.readline()
        temperature = temperature.splitlines()
        return temperature[0]

    def end_stage(self):
        self.comunication_serial.write("end".encode())
        time.sleep(2)
