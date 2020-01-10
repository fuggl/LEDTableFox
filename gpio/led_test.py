from rpi_ws281x import Color, PixelStrip, ws

# LED strip configuration:
LED_COUNT = 240  # Number of LED pixels.
LED_PIN = 13  # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1
# LED_STRIP = ws.SK6812_STRIP_RGBW
LED_STRIP = ws.SK6812W_STRIP

# LED start indexes by seat
SEAT_COUNT = 6
# fill manually and comment out call in init() when not regular
SEAT_LED_START = []  # LED starting indexes per seat
SEAT_LED_COUNT = []  # LED counts per seat

strip = "PixelStrip(0, 0)"


def set_color(first=0, led_count=LED_COUNT, color=Color(0, 0, 0, 0), show=True):
    print("set {} LEDs, starting at {} to {} (show = {})".format(led_count, first, color, show))


def set_seat_color(seat_nr, color, show=True):
    print("set LEDs of seat {} to {} (show = {})".format(seat_nr, color, show))


def regular_led_count_per_seat():
    seat_idx = 0
    offset = 0
    led_per_seat = int(LED_COUNT / SEAT_COUNT)
    while seat_idx < SEAT_COUNT:
        SEAT_LED_START.append(offset)
        SEAT_LED_COUNT.append(led_per_seat)
        seat_idx += 1
        offset += led_per_seat


def init():
    regular_led_count_per_seat()
    set_color(Color(0, 0, 0, 0))
