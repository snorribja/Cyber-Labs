import time
import spidev
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

CS_PIN = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.output(CS_PIN, GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

i2c = busio.I2C(board.SCL, board.SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

VOLTAGE_MAX = 5.0
ADC_RESOLUTION = 1023

def distance_from_voltage(voltage):
    distance =?13.69 * voltage**2 - 95.42 * voltage + 187.76

def read_adc(channel):
    GPIO.output(CS_PIN, GPIO.LOW)
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    GPIO.output(CS_PIN, GPIO.HIGH)
    return data

def voltage_from_adc(adc_value):
    return (adc_value * VOLTAGE_MAX) / ADC_RESOLUTION

def update_display(distance, voltage):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if distance == -1:
        text = "Out of range"
    else:
        text = "Distance: {} cm \nVoltage: {} v".format(distance, voltage)
    draw.text((0, 0), text, font=font, fill=255)
    disp.image(image)
    disp.show()

def main():
    try:
        while True:
            adc_value = read_adc(0)
            voltage = voltage_from_adc(adc_value)
            distance = distance_from_voltage(voltage)
            if distance == -1:
                print(f"ADC: {adc_value}, Voltage: {voltage:.2f}V, Distance: Out of range")
            else:
                print(f"ADC: {adc_value}, Voltage: {voltage:.2f}V, Distance: {distance} cm")
            update_display(distance, voltage)
            time.sleep(1)
    except KeyboardInterrupt:
        disp.fill(0)
        disp.show()
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
