from rpi_ws281x import *

LED_COUNT = 66
LED_PIN = 18
LED_FREQ = 800000
LED_DMA = 10

LED_BRIGHTNESS = 65
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_Neopixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

for i in range(0, LED_COUNT):
    strip.setPixelColor(i, Color(0,255,0))

strip.show()
