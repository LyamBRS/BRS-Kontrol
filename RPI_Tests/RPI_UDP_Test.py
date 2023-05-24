import socket
import time

UDP_IP = "0.0.0.0"  # Bind to all available network interfaces
UDP_PORT = 4210  # Specify the port number you want to receive messages on

DELAY = 0
READINGS = 10
TIMEOUT = 5



# Create a UDP socket
Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout of 5 seconds for the socket
Socket.settimeout(TIMEOUT)

# Bind the socket to the IP address and port
Socket.bind((UDP_IP, UDP_PORT))

print("UDP server started. Waiting for incoming messages...")

for i in range(READINGS):
    # Receive data and the address of the sender
    print(f"======================================[{i} / {READINGS}]")
    try:
        data, addr = Socket.recvfrom(1024)  # Adjust the buffer size as per your requirements
        message = data.decode("utf-8")
        # Print the received message and the sender's address
        print("Received message:", message)
        print("Sender address:", addr)
    except TimeoutError as e:
        print(f">>> Timedout after {TIMEOUT}")
    # Decode the received data assuming it's in UTF-8 encoding

    time.sleep(DELAY)

# Close the socket (this part of the code won't be reached in the current setup)
Socket.close()