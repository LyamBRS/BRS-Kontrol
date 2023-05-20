import time
from pynput.keyboard import Controller

# Function to simulate keyboard inputs with a delay between each key press
def send_keys_with_delay(keys, delay):
    keyboard = Controller()
    for key in keys:
        keyboard.press(key)
        time.sleep(delay)
        keyboard.release(key)
        time.sleep(delay)

# Run sudo raspi-config command
command = "sudo raspi-config"
keyboard = Controller()
keyboard.type(command)
keyboard.press(keyboard.enter)
keyboard.release(keyboard.enter)
time.sleep(1)

# Send left-arrow, left-arrow, and enter keys with a delay of 1 second
keys = [keyboard.left, keyboard.left, keyboard.enter]
send_keys_with_delay(keys, 1)