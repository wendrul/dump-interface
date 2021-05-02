import serial, time, sys


class PooperInterface:
    def __init__(self, baudrate=115200, port='COM4', timeout = 2):
        print(f"Opening connection o serial port '{port}' at baud {baudrate}...", file=sys.stderr)
        self.ser = serial.Serial(port, baudrate, timeout=timeout, write_timeout=timeout)
        print("Connection succesful", file=sys.stderr)
        self.sitting = False
        self.paperRollWeight = -1
        time.sleep(3)
   
    def UpdateStatus(self):
        """
        Call this periodically to read the serial port and update the class members
        """
        line = None
        while (self.ser.in_waiting):
            line = self.ser.readline().decode()
        if (line != None):
            L = str(line).split(',')
            for u in L:
                if ("sitting" in u):
                    self.sitting = "true" in u
                if ("paperWeight" in u):
                    self.paperRollWeight = float(u.split(' ')[-1])

    def IsSitting(self):
        return self.sitting

    def CloseConnection(self):
        self.ser.close()
        print("Connection Closed", file=sys.stderr)
