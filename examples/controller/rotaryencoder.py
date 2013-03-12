#----------------------------------------------------------------------
# rotary_encoder.py from https://github.com/guyc/py-gaugette
# Guy Carpenter, Clearwater Software
#
# This is a class for reading quadrature rotary encoders
# like the PEC11 Series available from Adafruit:
#   http://www.adafruit.com/products/377
# The datasheet for this encoder is here:
#   http://www.adafruit.com/datasheets/pec11.pdf
#
# This library expects the common pin C to be connected
# to ground.  Pins A and B will have their pull-up resistor
# pulled high.
# 
# Usage:
#
#     import gaugette.rotary_encoder
#     A_PIN = 7  # use wiring pin numbers here
#     B_PIN = 9
#     encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
#     while 1:
#       delta = encoder.delta() # returns 0,1,or -1
#       if delta!=0:
#         print delta

import RPi.GPIO as GPIO
import math
import threading
import time
import gpio_map

class RotaryEncoder:

    #----------------------------------------------------------------------
    # Pass the wiring pin numbers here.  See:
    #  https://projects.drogon.net/raspberry-pi/wiringpi/pins/
    #----------------------------------------------------------------------
    def __init__(self, a_pin, b_pin):
        self.a_pin = a_pin
        self.b_pin = b_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.last_delta = 0
        self.r_seq = self.rotation_sequence()

    # Gets the 2-bit rotation state of the current position
    # This is deprecated - we now use rotation_sequence instead.
#    def rotation_state(self):
#        a_state = self.gpio.digitalRead(self.a_pin)
#        b_state = self.gpio.digitalRead(self.b_pin)
#        r_state = a_state | b_state << 1
#        return r_state

    # Returns the quadrature encoder state converted into
    # a numerical sequence 0,1,2,3,0,1,2,3...
    #    
    # Turning the encoder clockwise generates these
    # values for switches B and A:
    #  B A
    #  0 0
    #  0 1
    #  1 1
    #  1 0 
    # We convert these to an ordinal sequence number by returning
    #   seq = (A ^ B) | B << 2
    # 
    def rotation_sequence(self):
        a_state = GPIO.input( self.a_pin)
        b_state = GPIO.input( self.b_pin)
        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq

    # Returns offset values of -2,-1,0,1,2
    def get_delta(self):
        delta = 0
        a_state = False
        b_state = False
        while True:
          a_state = GPIO.input( self.a_pin)
          b_state = GPIO.input( self.b_pin)
          r_seq = (a_state ^ b_state) | b_state << 1
          if r_seq != self.r_seq:

            step = (r_seq - self.r_seq) % 4
            if step==3:
                step = -1
            elif step ==2:
				# bad sample, ignore it
                step = 0               

            self.r_seq = r_seq
 #           print 'delta ' + str(delta) + ' ' + str(r_seq) + ' ' + str(a_state) + ' ' + str(b_state)
            if (a_state and b_state):
              # at detent, report back
              break 
            else:
			  # between detents, keep sampling	
              delta = delta + step

          self.last_delta = delta


 #       print 'finally ' + str(r_seq) + ' ' + str(a_state) + ' ' + str(b_state)
        return delta

    class Worker(threading.Thread):
        def __init__(self, a_pin, b_pin):
            threading.Thread.__init__(self)
            self.lock = threading.Lock()
            self.encoder = RotaryEncoder(a_pin, b_pin)
            self.daemon = True
            self.delta = 0

        def run(self):
            while True:
                delta = self.encoder.get_delta()
                with self.lock:
                    self.delta += delta
                time.sleep(0.001)

        def get_delta(self):
            # revisit - should use locking
            with self.lock:
                delta = self.delta
                self.delta = 0
            return delta


def main():

#  encoder = RotaryEncoder(ENCODER_A, ENCODER_B)
  encoder = RotaryEncoder.Worker( gpio_map.ENCODER_A, gpio_map.ENCODER_B)
  encoder.start()
  last_state = None

  while True:
    delta = encoder.get_delta()
    if delta!=0:
        print "rotate %d" % delta


if __name__ == '__main__':
  main()
