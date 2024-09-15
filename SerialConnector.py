import serial


class SerialConnector:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate)

    def read(self):
        return self.serial.readline()

    def write(self, data):
        self.serial.write(data)

    def close(self):
        self.serial.close()

if __name__ == '__main__':
    serialConnector = SerialConnector('COM1', 9600)
    serialConnector.write(b'Hello')
    #print(serialConnector.read())
    serialConnector.close()