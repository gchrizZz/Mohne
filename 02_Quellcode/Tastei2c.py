import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sys, tty, termios, time
import smbus
import time
bus = smbus.SMBus(1)
address = 0x04


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
    if(char == "w"):
      
        writeNumber(int(1))
        

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
       
       writeNumber(int(4))

    # The "a" key will toggle the steering left
    if(char == "a"):
       
        writeNumber(int(2))


    # The "d" key will toggle the steering right
    if(char == "d"):
        
        writeNumber(int(3))

    # The "q" key will bremsen
    if(char == "q"):
    
        writeNumber(int(5))
        
      

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        writeNumber(int(6))
        break


    char = ""

# Program will cease all GPIO activity before terminating
GPIO.cleanup()

