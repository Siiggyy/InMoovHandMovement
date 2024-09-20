import serial
import time

# Set the correct port and baud rate
arduino = serial.Serial('COM5', 9600, timeout=1)  # Replace 'COM3' with your port

time.sleep(2)  # Give some time to establish the connection

dataarray = [42,
353,
529,
704,
870

]
# Test sending data
for entry in dataarray:
    data = f"{entry}\n"
    arduino.write(data.encode())
    time.sleep(1)
data = "63\n"  # This data should move the index finger
arduino.write(data.encode())

# Wait for Arduino to respond (if any response is expected)
time.sleep(1)

arduino.close()
