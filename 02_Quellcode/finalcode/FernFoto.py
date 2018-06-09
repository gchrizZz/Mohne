eimport RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import smbus
import time
import sys
import os
from twython import Twython
from random import choice

bus = smbus.SMBus(1)
address = 0x04

replies = ['You shall not pass #Mohne',
           'One does not simply drive autonomously #Mohne',
           'Thats one small step for a drone, one giant leap for mankind #Mohne',
           'My humans think they can control me muahahaha #Mohne',
           'The human race may be the only intelligent beings in the galaxy - Stephen Hawking. Yeah....about that...'
        ]
consumer_key = 'VJmX2Ip8bK9A7dO8ON4SxzcJJ'
consumer_secret = 'gBC9TXEqhmzM37PGQKV8rpuqTm0tKlavKTNrV0gtrBR5t0LG4I'
access_token = '992389516777357313-7IsnQuFKB58hTl8JWXQwxpZK0J9pA1U'
access_token_secret = 'N87JxbTxX8oykSHW4UkXeBaMoXHjNkCOWERjGZZGaeTbB'

from pynput import keyboard

def writeNumber(value):
    bus.write_byte(address, value)

    return -1

def readNumber():
        nummer = bus.read_byte(address)
        return nummer
  

def on_key_press(key): 
        if key == keyboard.Key.right:
            
            writeNumber(int(2))
                      
        if key == keyboard.Key.up:
            
            writeNumber(int(1))
         
        if key == keyboard.Key.down:
            
            writeNumber(int(4))
          
        if key == keyboard.Key.left:
            
            writeNumber(int(3))
     
        if key == keyboard.Key.esc:
            writeNumber(int(5))
            print("Mohne sagt Ciao")
            sys.exit("Mohne sagt Ciao")
            
        if key == keyboard.Key.space:
            takephoto = "raspistill -o /home/pi/picture.jpg"
            os.system(takephoto)
            photo = open('/home/pi/picture.jpg', 'rb')
            twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
            image = twitter.upload_media(media=photo)
            twitter.update_status(status=(choice(replies)), media_ids=[image['media_id']])
          
        else:
           writeNumber(int(5))
           
               
            
def on_key_release(key):
    #motor aus
    writeNumber(int(5))
   


with keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release) as listener:
    listener.join()
    
    
GPIO.cleanup()


