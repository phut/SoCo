
import RPi.GPIO as GPIO
import math
import threading
import time
import logging
import sys
from rotaryencoder import RotaryEncoder

import ui_out
import gpio_map
import sonoscontroller
from sonoseventhandler import CommandFilter
from ui_out_gpio import BlinkenLightsFilter
from ui_out_screen import LcdFilter

def init():
    gpio_map.ports_setup()
    
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
   
    log = sonoscontroller.log
    log.addFilter(CommandFilter())
    
    ch.setFormatter(formatter)
    sonoscontroller.log.addHandler(ch)
    sonoscontroller.log.setLevel(logging.INFO)
    
    ui_out.log.addFilter(BlinkenLightsFilter())
    ui_out.log.addFilter(LcdFilter())
    
def main():


  
  oo_state = GPIO.input( gpio_map.ON_OFF )
  push_state = GPIO.input( gpio_map.ENCODER_PUSH )
  
  if oo_state == gpio_map.PUH_ON:
    sonoscontroller.log.info( sonoscontroller.cmd_on)
  else:
    sonoscontroller.log.info( sonoscontroller.cmd_off)
  
  encoder = RotaryEncoder.Worker( gpio_map.ENCODER_A, gpio_map.ENCODER_B)
  encoder.start()


  while True:
    delta = encoder.get_delta()
    if delta!=0:
       print "rotate %d" % delta
       if delta > 0:
         sonoscontroller.log.info( sonoscontroller.cmd_next)
       else:
         sonoscontroller.log.info( sonoscontroller.cmd_previous)
       

    new_state = GPIO.input( gpio_map.ENCODER_PUSH )
    if push_state != new_state:
      push_state = new_state
      print 'click - ' + str( push_state)


    new_state = GPIO.input( gpio_map.ON_OFF )
    if oo_state != new_state:
      oo_state = new_state
      print 'on off - ' + str( oo_state)
      if oo_state == gpio_map.PUH_ON:
        sonoscontroller.log.info( sonoscontroller.cmd_on)
      else:
        sonoscontroller.log.info( sonoscontroller.cmd_off)

if __name__ == '__main__':
  init()
  main()
