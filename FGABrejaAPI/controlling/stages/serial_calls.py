from controlling.comunication import Comunication


class SerialCalls(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SerialCalls, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.serial_call = Comunication()

    def insert_water(self):
        self.serial_call.insert_water()

    def get_pot_level(self):
        pot_level = self.serial_call.get_pot_level()
        return pot_level

    def stop_water(self):
        self.serial_call.stop_water()

    def turn_on_engine(self):
        self.serial_call.turn_on_engine()

    def turn_off_engine(self):
        self.serial_call.turn_off_engine()

    def turn_on_resistor(self, temperature=None):
        if temperature is not None:
            self.serial_call.turn_on_resistor(temperature)
        else:
            self.serial_call.turn_on_resistor()

    def add_hop(self, engine_id):
        self.serial_call.add_hop(engine_id)

    def turn_off_resistor(self, pot):
        self.serial_call.turn_off_resistor(pot)

    def turn_on_chiller(self):
        self.serial_call.turn_on_chiller()

    def turn_off_chiller(self):
        self.serial_call.turn_off_chiller()

    def turn_on_freezer(self, temperature):
        self.serial_call.turn_on_freezer(temperature)

    def activate_alarm(self):
        self.serial_call.activate_alarm()

    def read_thermal_sensor(self):
        self.serial_call.read_thermal_sensor()

    def end_stage(self):
        self.serial_call.end_stage()
