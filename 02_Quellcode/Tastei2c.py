import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sys, tty, termios, time
import smbus
import time
bus = smbus.SMBus(1)
address = 0x04
#address2 = 0x05


#GPIO.setup(23,GPIO.OUT)  #w rot
#GPIO.setup(24,GPIO.OUT) #a gelb
#GPIO.setup(25,GPIO.OUT) #d gruen
#GPIO.setup(21,GPIO.OUT) #s blau

#GPIO.output(23,GPIO.LOW)  #w rot
#GPIO.output(24,GPIO.LOW) #a gelb
#GPIO.output(25,GPIO.LOW) #d gruen
#GPIO.output(21,GPIO.LOW) #s blau

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
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
        #GPIO.output(21, GPIO.LOW)
        #GPIO.output(23, GPIO.HIGH)
        #GPIO.output(24, GPIO.LOW)
        #GPIO.output(25, GPIO.LOW)
        writeNumber(int(1))
        #print(writeNumber)

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
        writeNumber(int(6))
        break


    char = ""

# Program will cease all GPIO activity before terminating
GPIO.cleanup()

