import sys
import os
from twython import Twython
from random import choice

# Hier werden die zu pushenden random replies definiert

replies = ['Platzhalter 1',
           'Platzhalter 2',
           'Platzhalter 3',
           'Platzhalter 4',
           'Platzhalter 5'
        ]

# Hier werden die Adressdaten von Twitter definiert

consumer_key = 'VJmX2Ip8bK9A7dO8ON4SxzcJJ'
consumer_secret = 'gBC9TXEqhmzM37PGQKV8rpuqTm0tKlavKTNrV0gtrBR5t0LG4I'
access_token = '992389516777357313-7IsnQuFKB58hTl8JWXQwxpZK0J9pA1U'
access_token_secret = 'N87JxbTxX8oykSHW4UkXeBaMoXHjNkCOWERjGZZGaeTbB'


# Foto machen und benennen

takephoto = "raspistill -o /home/pi/picture.jpg"
os.system(takephoto)
photo = open('/home/pi/picture.jpg', 'rb')

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

image = twitter.upload_media(media=photo)

twitter.update_status(status=(choice(replies)), media_ids=[image['media_id']])
