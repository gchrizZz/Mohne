import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sys, tty, termios, time
import smbus
import time
bus = smbus.SMBus(1)
address = 0x04

from pynput import keyboard


def writeNumber(value):
    bus.write_byte(address, value)
     
    return -1

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



while True:

    char = getch()
    
    # The car will drive forward when the "w" key is pressed
    #if(char == "w"):
     #   GPIO.output(21, GPIO.LOW)
      #  GPIO.output(23, GPIO.HIGH)
       # GPIO.output(24, GPIO.LOW)
        #GPIO.output(25, GPIO.LOW)
        #writeNumber(int(1))
        #print(writeNumber)
    def on_press(w):
        GPIO.output(21, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
    def on_release(w):
        GPIO.output(21, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
    with keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release) as listener:
        listener.join()

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
       # GPIO.output(21, GPIO.HIGH)
       # GPIO.output(23, GPIO.LOW)
        #GPIO.output(24, GPIO.LOW)
       # GPIO.output(25, GPIO.LOW)
       writeNumber(int(4))

    # The "a" key will toggle the steering left
    if(char == "a"):
        #GPIO.output(21, GPIO.LOW)
        #GPIO.output(23, GPIO.LOW)
        #GPIO.output(24, GPIO.HIGH)
        #GPIO.output(25, GPIO.LOW)
        writeNumber(int(2))


    # The "d" key will toggle the steering right
    if(char == "d"):
        #GPIO.output(21, GPIO.LOW)
        #GPIO.output(23, GPIO.LOW)
        #GPIO.output(24, GPIO.LOW)
        #GPIO.output(25, GPIO.HIGH)
        writeNumber(int(3))

    # The "q" key will bremsen
    if(char == "q"):
        #GPIO.output(21, GPIO.LOW)
        #GPIO.output(23, GPIO.LOW)
        #GPIO.output(24, GPIO.LOW)
        #GPIO.output(25, GPIO.LOW)
        writeNumber(int(5))
        
      

    # The "x" key will break the loop and exit the program
    if(char == "x"):

        break


    char = ""

# Program will cease all GPIO activity before terminating
GPIO.cleanup()

