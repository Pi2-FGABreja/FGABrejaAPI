import serial


class Comunication(object):

    def __init__(self):
        self.comunication_serial = serial.Serial(0)

    # Pre Brewery Stage Serial Comunication
    def insert_water(self):
        self.comunication_serial.write("insert_water")

    def get_pot_level(self):
        pot_level = self.comunication_serial.readline()
        return pot_level

    def stop_water(self):
        self.comunication_serial.write("stop_water")

    # Brewery Stage Serial Comunication
    def turn_on_engine(self):
        self.comunication_serial.write("turn_on_engine")

    def get_engine_state(self):
        engine_state = self.comunication_serial.readline()
        return engine_state

    def turn_on_resistor(self, pot, temperature=None):
        if temperature is not None:
            self.comunication_serial.write("turn_on_resistor , %s" % pot %
                                           "%.2f" % temperature)
        else:
            self.comunication_serial.write("turn_on_resistor , %s" % pot)

    # Boiling Stage Serial Comunication
    def add_hop(self, engine_id):
        self.comunication_serial.write("add_hop , %d" % engine_id)

    def turn_off_resistor(self, pot):
        self.comunication_serial.write("turn_off_resistor , %s" % pot)

    # Cooling Stage Serial Comunication
    def turn_on_chiller(self):
        self.comunication_serial.write("turn_on_chiller")

    def turn_off_chiller(self):
        self.comunication_serial.write("turn_off_chiller")

    # Fermentation Stage Serial Comunication
    def turn_on_freezer(self, temperature):
        self.comunication_serial.write("turn_on_freezer , %.2f" % temperature)

    # Common Stages Serial Comunication
    def activate_alarm(self):
        self.comunication_serial.write("activate_alarm")

    def read_thermal_sensor(self, location):
        self.comunication_serial.write("read_thermal_sensor , %s" % location)
        temperature = self.comunication_serial.readline()
        return temperature

    def end_stage(self, stage_name):
        self.comunication_serial.write("End %s" % stage_name)
