
import RPi.GPIO as GPIO
import math
import threading
import time
import gpio_map
import leds
from rotaryencoder import RotaryEncoder



def main():

  gpio_map.ports_setup()
  
  oo_state = GPIO.input( gpio_map.ON_OFF )
  push_state = GPIO.input( gpio_map.ENCODER_PUSH )
  
  encoder = RotaryEncoder.Worker( gpio_map.ENCODER_A, gpio_map.ENCODER_B)
  encoder.start()


  while True:
    delta = encoder.get_delta()
    if delta!=0:
       print "rotate %d" % delta

    new_state = GPIO.input( gpio_map.ENCODER_PUSH )
    if push_state != new_state:
      push_state = new_state
      print 'click - ' + str( push_state)


    new_state = GPIO.input( gpio_map.ON_OFF )
    if oo_state != new_state:
      oo_state = new_state
      print 'on off - ' + str( oo_state)

if __name__ == '__main__':
  main()
