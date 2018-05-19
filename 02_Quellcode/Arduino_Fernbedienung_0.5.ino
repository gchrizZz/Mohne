

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

//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
 // Wire.begin(SLAVE_ADDRESS2);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
   Wire.onRequest(sendData);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(Trigger_AusgangsPin, OUTPUT);
  pinMode(Echo_EingangsPin, INPUT);
}

void loop() {
  delay(100);
  digitalWrite(Trigger_AusgangsPin, HIGH);
 delayMicroseconds(10); 
 digitalWrite(Trigger_AusgangsPin, LOW);
  Dauer = pulseIn(Echo_EingangsPin, HIGH);
  
 // Nun wird der Abstand mittels der aufgenommenen Zeit berechnet
 Abstand = Dauer/58.2;
 
// if (Abstand < 20){
 // sendData();
  //Wire.write(int(9));
  //digitalWrite(10, HIGH);
  //Serial.print ("max ist immernoch doof");
//}
//  if (Abstand > 20){
    //Serial.print("max ist doof");
  //  digitalWrite(10, LOW);
   // Wire.write(int(10));
//  }
} // end loop

// callback for received data
void receiveData(int byteCount) {
  while (Wire.available()) {
    int number = Wire.read();
    if (number == 1){
   // digitalWrite(8, HIGH);
  //  Serial.print (number);
     }
    if (number == 2){
    digitalWrite(6, HIGH);
   // Serial.print (number);
    }
    if (number == 3){
    digitalWrite(4, HIGH);
   // Serial.print (number);
    }
    if (number == 4){
    digitalWrite(2, HIGH);
   // Serial.print (number);
    }
    if (number == 5){
      digitalWrite(2, LOW);
      digitalWrite(4, LOW);
      digitalWrite(6, LOW);
      digitalWrite(8, LOW);
      if (Abstand > 20){
        Wire.write(int(10));
      }
      if (Abstand < 20){
        Wire.write(int(9));
      }
    }
    /// else{
     // digitalWrite(2, LOW);
     // digitalWrite(4, LOW);
     // digitalWrite(6, LOW);
     // digitalWrite(8, LOW);
       
   // }
 }
  
  
  //
  Serial.print(number);
}  


// end while

// callback for sending data
void sendData() {
  if (Abstand < 20){
   //number == 9;
 Wire.write(int(9));
 digitalWrite(10, HIGH);
}
  if (Abstand > 20){
   Wire.write(int(10));
  }
}

//End of the program
