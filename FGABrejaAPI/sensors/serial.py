import serial


class SerialReader:
    def __init__(self, parameters):
        self.ser = None
        try:
            self.ser = serial.Serial(port='/dev/ttyAMA0',
                                     baudrate=9600,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS, timeout=1)
        except:
            self.ser = None
            print 'Failed to connect to serial port'

    def read_serial(self):
        x = self.ser.readline().strip()
        print(x)
