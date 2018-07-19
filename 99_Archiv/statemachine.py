import os, time, sys
#import threading
import minimalmodbus
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from statemachine import StateMachine, State

####################################
##### Mqtt Communication Setup #####
####################################

# The callbackresponse from the server.
Connected = False
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
        Connected = True
        client.subscribe("Chargingstation1")
    else:
        print("Connection failed")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Disconnect message
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# Publish callback
def on_publish(client, userdate, mid):
    print(mid)
    
# Setup mqtt connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.connect("128.127.67.86", 1883, 60)

########################
##### Statemachine #####
########################

class mqttstate(StateMachine):
    donothing = State ("Sleep", initial=True) 
    loadingpv = State("Loadingpv")#("20,1,info")
    
#States which results in publishing mqtt    
    authstart= State("3,1")
    loadingstatusmixed = State("7,1,info")
    stoprequest = State("10,1")
    sendingcdr = State("14,1")
    
#States which needs a mqtt subscription
    startfromapp = State("1")
    authorizedstartyes = State("1,0")
    authorizedstartno = State("1,1")
    ackstop = State("2")
    
    dntoloadingpv = donothing.to(loadingpv)
    lpvtostartfapp = loadingpv.to(startfromapp)
    startfapptoauthstart = startfromapp.to(authstart)
    authstarttoyes = authstart.to(authorizedstartyes)
    authstarttono = authstart.to(authorizedstartno)
    yestolmixed = authorizedstartyes.to(loadingstatusmixed)
    lmixedtostopreq = loadingstatusmixed.to(stoprequest)
    stopreqtoackstop = stoprequest.to(ackstop)
    ackstoptocdr = ackstop.to(sendingcdr)
    
    #def on_donothing(self):
        #print("Ich mache gerade nichtes, weil kein kabel angesteckt ist")
        
    def on_dntoloadingpv(self):
        print("Lade gruen")
        client.loop_start()
        client.publish("AUDICPO","20,1,info")
        time.sleep(1)
        
    def on_startfapptoauthstart(self):
        client.loop_start()
        client.publish("AUDICPO","2,1")
        client.loop_stop()
        
    def on_startfapptoauthstart(self):
        client.loop_start()
        client.publish("AUDICPO","7,1,info")
        time.sleep(1)
        
    def on_stoprequest(self):
        client.loop_start()
        client.publish("AUDICPO",",")
        client.loop_stop()
        
    def on_sendingcdr(self):
        client.loop_start()
        client.publish("AUDICPO",",,CDRData")
        client.loop_stop()
        
    def on_lpvtostartfapp(self):
        print("Mixed-Ladeanfrage von der APP")
    def on_authstarttoyes(self):
        print("Ladeerlaubnis von Hubject erhalten")     
    def on_authorizedstartno(self):
        print("Keine Ladeerlaubnis von Hubject erhalten")
    def on_ackdstop(self):
        print("Stopacknowledge von Hubject erhalten")
        
msm = mqttstate()

#client.loop_start()
try:
    msm.dntoloadingpv()
    if msn.lpvtostartapp = 1
                
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()