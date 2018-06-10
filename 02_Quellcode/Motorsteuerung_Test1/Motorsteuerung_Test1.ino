#include <Servo.h> 
 
//Create the 4 esc objects
Servo esc1;
Servo esc2;
Servo esc3;
Servo esc4;
 
//Esc pins
int escPin1 = 5;
int escPin2 = 6;
int escPin3 = 10;
int escPin4 = 11;
int Trigger_Ausgangspin1 = 0;
int Echo_EingangsPin1 = 0;
int Trigger_Ausgangspin2 = 0;
int Echo_EingangsPin2 = 0;
int cm;

long maximumRange = 10;
long minimumRange = 5;
long Abstand;
long Abstand1;
long Abstand2;
long Dauer1;
long Dauer2;
long duration;

const int pingPin1 = 7;
const int pingPin2 = 7;


//Min and max pulse
int minPulseRate        = 1000;
int maxPulseRate        = 2000;
int throttleChangeDelay = 50;
 
//SETUP
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  
  //Init escs
  initEscs();
}
 
//LOOP
void loop() {
  // Wait for some input
  if (Serial.available() > 0) {
    
    // Read the new throttle value
    int throttle = normalizeThrottle(Serial.parseInt());
    
    // Print it out
    Serial.print("Setting throttle to: ");
    Serial.println(throttle);
    
    // Change throttle to the new value
    changeThrottle(throttle);

  // establish variables for duration of the ping, and the distance result
  // in inches and centimeters:
  long duration, cm;
  }
  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin1, OUTPUT);
  digitalWrite(pingPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin1, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin1, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH pulse
  // whose duration is the time (in microseconds) from the sending of the ping
  // to the reception of its echo off of an object.
  pinMode(pingPin2, INPUT);
  duration = pulseIn(pingPin2, HIGH);

  // convert the time into a distance
  cm = microsecondsToCentimeters(duration);

  Serial.print(cm);
  Serial.print("cm");
  Serial.println();

  //delay(100);
  
  if (Abstand1 == Abstand2)
    {
        digitalWrite(escPin1, HIGH);
        digitalWrite(escPin2, HIGH);
        digitalWrite(escPin3, HIGH);
        digitalWrite(escPin4, HIGH);
        //delay(1000);
}

    else if (Abstand1 < Abstand2 )
    {
        // Umkehrschub, Fahrzeug bremst.
        digitalWrite(escPin1, HIGH);
        digitalWrite(escPin2, HIGH);
        digitalWrite(escPin3, HIGH);
        digitalWrite(escPin4, HIGH);
        //delay(1000);
   }
}


long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the object we
  // take half of the distance travelled.
  return microseconds / 29 / 2;
}
 
//Change throttle value
void changeThrottle(int throttle) {
  int currentThrottle = readThrottle();
  
  int step = 1;
  if(throttle < currentThrottle) {
    step = -1;
  }
  
  // Slowly move to the new throttle value 
  while(currentThrottle != throttle) {
    writeTo4Escs(currentThrottle + step);
    
    currentThrottle = readThrottle();
    delay(throttleChangeDelay);
  }
}

//Read the throttle value
int readThrottle() {
  int throttle = esc1.read();
  
  Serial.print("Current throttle is: ");
  Serial.print(throttle);
  Serial.println();
  
  return throttle;
}

//Change velocity of the 4 escs at the same time
void writeTo4Escs(int throttle) {
  esc1.write(throttle);
  esc2.write(throttle);
  esc3.write(throttle);
  esc4.write(throttle);
}

//Init escs
void initEscs() {
  esc1.attach(escPin1, minPulseRate, maxPulseRate);
  esc2.attach(escPin2, minPulseRate, maxPulseRate);
  esc3.attach(escPin3, minPulseRate, maxPulseRate);
  esc4.attach(escPin4, minPulseRate, maxPulseRate);
  
  //Init motors with 0 value
  writeTo4Escs(0);
}

//Start the motors
void startUpMotors() {
  writeTo4Escs(50);
}
 
// Ensure the throttle value is between 0 - 180
int normalizeThrottle(int value) {
  if(value < 0) {
    return 0;
    
  } else if(value > 180) {
    return 180;
  }
  
  return value;
}





