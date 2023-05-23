import serial
import time

# Define the serial port configurations
serial_ports = [
    "/dev/ttyAMA0",  # Serial 0
    "/dev/ttyAMA1",  # Serial 1
    "/dev/ttyAMA2",  # Serial 2
    "/dev/ttyAMA3",  # Serial 3
    "/dev/ttyAMA4",  # Serial 4
    "/dev/ttyAMA5"   # Serial 5
]

# Define the characters to output
characters = ["A", "B", "C", "D", "E", "F"]

print("========================================== - [BRS]")
print("Sending A,B,C,D,E at 9600 baud on serial ports...")
# Open each serial port and send the corresponding character
for port, character in zip(serial_ports, characters):
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        ser.write(character.encode())
        ser.close()
        print(f">>> Character {character} sent on {port}")
    except serial.SerialException as e:
        print(f">>> Failed to send on port {port}")
    time.sleep(0.5)  # Add a delay between sending characters

print("\n")
print("All characters sent.")
print("========================================== - [BRS]")