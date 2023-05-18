import time
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA, 10)

detected = i2c.scan()

print(f"detected i2c devices: {detected}")
if(len(detected) == 0):
    print("No i2c devices were detected... rip...")
else:
    print("Something was detected.")

accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    print("%f %f %f"%accelerometer.acceleration)
    time.sleep(1)

i2c.deinit()