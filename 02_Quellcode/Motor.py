# include <Servo.h>


#Create the 4 esc objects
Servo_esc1;
Servo_esc2;
Servo_esc3;
Servo_esc4;

#Esc pins
int escPin1 = 5;
int escPin2 = 6;
int escPin3 = 10;
int escPin4 = 11;

int trigger = 7
int echo = 6
long dauer = 0
long entfernung = 0


#Min and max pulse
int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 50;

#SETUP
void setup() {
    Serial.begin(9600);
    Serial.setTimeout(500);

#Init escs
initEscs();
}

#LOOP
void loop() {
#Wait
    for some input
    if (Serial.available() > 0) {

    #Read the new throttle value
    int throttle = normalizeThrottle(Serial.parseInt());

    #Print it out
    Serial.print("Setting throttle to: ");
    Serial.println(throttle);

    #Change throttle to the new value
    changeThrottle(throttle);
    }

   }

#Change throttle value
void changeThrottle(int throttle) {
    int currentThrottle = readThrottle();

    int step = 1;
    if (throttle < currentThrottle) {
    step = -1;
    }

#Slowly move to the new throttle value
    while (currentThrottle != throttle) {
        writeTo4Escs(currentThrottle + step);

        currentThrottle = readThrottle();
        delay(throttleChangeDelay);
       }
     }

#Read the throttle value
int readThrottle() {
    int throttle = esc1.read();

    Serial.print("Current throttle is: ");
    Serial.print(throttle);
    Serial.println();

    return throttle;
}

#Change velocity of the 4 escs at the same time
void writeTo4Escs(int throttle) {
    esc1.write(throttle);
    esc2.write(throttle);
    esc3.write(throttle);
    esc4.write(throttle);
}

#Init escs
void initEscs() {
    esc1.attach(escPin1, minPulseRate, maxPulseRate);
    esc2.attach(escPin2, minPulseRate, maxPulseRate);
    esc3.attach(escPin3, minPulseRate, maxPulseRate);
    esc4.attach(escPin4, minPulseRate, maxPulseRate);

#Init motors with 0 value
    writeTo4Escs(0);
}

#Start the motors
void
startUpMotors() {
    writeTo4Escs(50);
   }

#Ensure the throttle value is between 0 - 180
int normalizeThrottle(int value) {
    if (value < 0) {
        return 0;

    } else if (value > 180) {
    return 180;
    }

    return value;
   }






void setup()
{
Serial.begin (9600)
pinMode(trigger, OUTPUT)
pinMode(echo, INPUT)
}
void loop()
{
digitalWrite(trigger, LOW)
delay(5)
digitalWrite(trigger, HIGH)
delay(10)
digitalWrite(trigger, LOW)
dauer = pulseIn(echo, HIGH)
entfernung = (dauer/2) * 0.03432  #Abstand in mm



if (entfernung >= 800) #|| entfernung <= 0)
#{
#Serial.println("Kein Messwert")
#}
#else
#{
#Serial.print(entfernung)
#Serial.println(" cm")
#}
#delay(1000)
#}
{
writeToEscs(180)       
}


else (entfernung <= 800) #|| entfernung >=0) 
{
    writeTo4Escs(0);
}

while (entfernung <= 800)
    esc1.write(0);
    esc2.write(180);
    esc3.write(180);
    esc4.write(0);
