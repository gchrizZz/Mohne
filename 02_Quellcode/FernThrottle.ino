#include <Servo.h> 
#define Echo_EingangsPin 11
#define Trigger_AusgangsPin 12 
/*
  I2C Pinouts

  SDA -> A4
  SCL -> A5
*/

//Import the library required
#include <Wire.h>

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x04
#define SLAVE_ADDRESS2 0x05

char number[50];
int state = 0;
int state2 = 0;
int nummer = 0;
long Abstand;
long Dauer;

//Create the 4 esc objects
Servo esc1;  //linksvorne
Servo esc2;   //linkhinten
Servo esc3;   //rechtsvorne
Servo esc4; //rechtshinten
 
//Esc pins
int escPin1 = 5;
int escPin2 = 6;
int escPin3 = 10;
int escPin4 = 11;

//Min and max pulse
int minPulseRate        = 1000;
int maxPulseRate        = 2000;
int throttleChangeDelay = 50;

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
void vornefahren(int throttle) {
  esc1.write(throttle);
  esc2.write(throttle);
  esc3.write(throttle);
  esc4.write(throttle);
}
//Init escs


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

void initEscs() {
  esc1.attach(escPin1, minPulseRate, maxPulseRate);
  esc2.attach(escPin2, minPulseRate, maxPulseRate);
  esc3.attach(escPin3, minPulseRate, maxPulseRate);
  esc4.attach(escPin4, minPulseRate, maxPulseRate);
  
  //Init motors with 0 value
  writeTo4Escs(0);
}
 
//SETUP
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  Wire.begin(SLAVE_ADDRESS);
 // Wire.begin(SLAVE_ADDRESS2);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
//   Wire.onRequest(sendData);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(Trigger_AusgangsPin, OUTPUT);
  pinMode(Echo_EingangsPin, INPUT);
  //Init escs
  initEscs();
}
 
//LOOP
void loop() {

   delay(100);
  digitalWrite(Trigger_AusgangsPin, HIGH);
 delayMicroseconds(10); 
 digitalWrite(Trigger_AusgangsPin, LOW);
  Dauer = pulseIn(Echo_EingangsPin, HIGH);
  // Wait for some input
  if (Serial.available() > 0) {
    
    // Read the new throttle value
    int throttle = normalizeThrottle(Serial.parseInt());
    
    // Print it out
    Serial.print("Setting throttle to: ");
    Serial.println(throttle);
    
    // Change throttle to the new value
    changeThrottle(throttle);
  }
 
}
 void receiveData(int byteCount) {
  while (Wire.available()) {
    int number = Wire.read();
    if (number == 1){    //vorne
   // digitalWrite(8, HIGH);
  //  Serial.print (number);
     }
    if (number == 2){
    digitalWrite(6, HIGH);  //rechts
   // Serial.print (number);
    }
    if (number == 3){   //links
    digitalWrite(4, HIGH);
   // Serial.print (number);
    }
    if (number == 4){  //hinten
    digitalWrite(2, HIGH);
   // Serial.print (number);
    }
    if (number == 5){   //keininput
      digitalWrite(2, LOW);
      digitalWrite(4, LOW);
      digitalWrite(6, LOW);
      digitalWrite(8, LOW);
     
    }
   
 }
 }

