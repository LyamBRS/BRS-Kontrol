import serial
import time

# Define the serial port configurations
serial_ports = [
    "/dev/ttyAMA0",  # Serial 1
    "/dev/ttyAMA1",  # Serial 2
    "/dev/ttyAMA2",  # Serial 3
    "/dev/ttyAMA3",  # Serial 4
    "/dev/ttyAMA4"   # Serial 5
]

# Define the characters to output
characters = ["A", "B", "C", "D", "E"]

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
        print(f">>> Error opening {port}: {str(e)}")
    time.sleep(1)  # Add a delay between sending characters

print("\n")
print("All characters sent.")
print("========================================== - [BRS]")