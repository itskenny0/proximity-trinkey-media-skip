import time
import board
import neopixel
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()  # uses board.SCL and board.SDA
apds = APDS9960(i2c)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 2)
consumer_control = ConsumerControl(usb_hid.devices)

apds.enable_proximity = True
apds.proximity_gain = 3
next_song = False

def proximity_to_brightness(value):
    """Maps the proximity values (0 - 255) to the brightness values (0.0 - 1.0)"""        
    return value / 255 * 1.5

while True:
    pixels.fill((0, 0, 255))
    print(apds.proximity)
    pixels.brightness = proximity_to_brightness(apds.proximity)
    if apds.proximity > 50:
        pixels.fill((255, 255, 255))
    if apds.proximity > 40 and not next_song:
        consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        pixels.brightness = 0.02
        pixels.fill((7, 247, 31))
        time.sleep(1)
        pixels.fill((255, 0, 0))
    time.sleep(0.02)
