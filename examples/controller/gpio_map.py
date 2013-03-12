import RPi.GPIO as GPIO

GPIO2  = 2  # (pin 03)(I2C1_SDA)
GPIO3  = 3  # (pin 05)(I2C1_SDL)
GPIO4  = 4  # (pin 07)(GPCLK0)
GPIO7  = 7  # (pin 26)
GPIO8  = 8  # (pin 24) 
GPIO9  = 9  # (pin 21)(SPI0_MISO)
GPIO10 = 10 # (pin 19)(SPI0_MOSI) 
GPIO17 = 17 # (pin 11) 
GPIO14 = 14 # (pin 08)(UART0_TXD)
GPIO18 = 18 # (pin 12)(PCM_CLK)
GPIO25 = 25 # (pin 22)  


#LED CONFIG - Set GPIO Ports
POWER_LED    = GPIO17   
FAULT_LED    = GPIO7  

ON_OFF       = GPIO8
ENCODER_A    = GPIO9
ENCODER_B    = GPIO10
ENCODER_PUSH = GPIO25

LED    = [POWER_LED,FAULT_LED]
SWITCH = [ON_OFF, ENCODER_A, ENCODER_B, ENCODER_PUSH]

PUH_ON  = 0
PUH_OFF = 1

def ports_setup():
  #Set up the wiring
  GPIO.setmode(GPIO.BCM)
  # Setup Ports
  for val in LED:
    GPIO.setup(val, GPIO.OUT, initial=GPIO.LOW)
  for val in SWITCH:
    GPIO.setup(val, GPIO.IN, pull_up_down=GPIO.PUD_UP)
