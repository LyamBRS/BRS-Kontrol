import serial
import time

# Define the serial port configurations
serial_ports = [
    "/dev/ttyAMA0",  # Serial 0 -> A -> TX1_B / RX1_B
    "/dev/ttyAMA2",  # Serial 2 -> D -> DEBUG
    "/dev/ttyAMA3",  # Serial 3 -> C -> TX1_A / RX1_A
    "/dev/ttyAMA4",  # Serial 4 -> E -> TX2_B / RX2_B
    "/dev/ttyAMA5"   # Serial 5 -> F -> TX2_A / RX2_A
]

# Define the characters to output
characters = {
    "/dev/ttyAMA0" : "TX1_B",
    "/dev/ttyAMA2" : "DEBUG",
    "/dev/ttyAMA3" : "TX1_A",
    "/dev/ttyAMA4" : "TX2_B",
    "/dev/ttyAMA5" : "TX2_A", 
}

print("========================================== - [BRS]")
print("Sending at 9600 baud on serial ports...")
# Open each serial port and send the corresponding character
for port, character in characters.items():
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