#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from threading import Thread
from threading import Event

import gpio_map

#Setup Active states
#Common Cathode RGB-LEDs (Cathode=Active Low)
LED_ENABLE = GPIO.HIGH
LED_DISABLE = GPIO.LOW






blinking=[]
flashing=[]
run=True



def flash_worker( trigger):
    while run:
      trigger.wait()
      while flashing or blinking:
        for led in flashing: led_activate(led)
        for led in blinking: led_activate(led)
        time.sleep(0.1)
        for led in blinking:
          led_deactivate(led)
        time.sleep(0.4)
        for led in flashing:
          led_deactivate(led)
        time.sleep(0.5)
      #TODO move clear to main thread to avoid race 
      trigger.clear()

def flash(led):
  #TODO check for duplication
  flashing.append( led)
  e.set()

def blink(led):
  #TODO check for duplication
  blinking.append( led)
  e.set()

def on(led):
  if led in flashing: flashing.remove( led)
  if led in blinking: blinking.remove( led)
  led_activate(led)
  #TODO check if anythign is flashing or blining, call clear.
     
def off(led):
  if led in flashing: flashing.remove( led)
  if led in blinking: blinking.remove( led)
  led_deactivate(led)
  #TODO check if anythign is flashing or blining, call clear.

def led_deactivate(led):
  GPIO.output(led,LED_DISABLE)

def led_activate(led):
  GPIO.output(led,LED_ENABLE)

def shutdown():
  #TODO remove unnecessary globals, call 'off', no need to check thread is running?
  #TODO contrary to the above maybe it's good to check either run or thread alive in case this called twice 
  global t
  global run

  if t.isAlive():
    for val in gpio_map.LED:
      GPIO.output(val, LED_DISABLE)
    del flashing[:]
    del blinking[:]
    run = False
    e.set
    t.join()
    # comment this out - maybe the inputs are still in use?
    # GPIO.cleanup()

def init():
  global e
  global t
  gpio_map.ports_setup()
  e = Event()
  t = Thread(target=flash_worker, args=(e,))
  t.daemon = True 
  t.start()

def test():


  led_activate(gpio_map.POWER_LED)
  led_activate(gpio_map.FAULT_LED)
  
#  GPIO.set_high_event(ENCODER_A)
#  GPIO.set_high_event(ENCODER_B)

  
#  led_deactivate(POWER_LED)
#  led_activate(POWER_LED)
  flash( gpio_map.FAULT_LED)
  blink( gpio_map.POWER_LED)
  time.sleep(5)
  

  on(gpio_map.POWER_LED)
  off(gpio_map.FAULT_LED)
  time.sleep(2)
  off(gpio_map.POWER_LED)
  blink( gpio_map.FAULT_LED)
  time.sleep(5)


  flash(gpio_map.POWER_LED)
  on( gpio_map.FAULT_LED)
  time.sleep(5)

#  led_deactivate(POWER_LED)
#  led_deactivate(FAULT_LED)
  shutdown()





if __name__ == '__main__':
  init()
  test()

#End
