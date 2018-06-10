#include <Servo.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x04
//motor 2 links vorne
//motor 1 rechts vorne
//motor 3 rechts hinten
// motor 4


int motor1_A=11; 
int motor1_B=10;
int motor1_Speed=9;

int motor3_Speed=2;
int motor3_B=4;
int motor3_A=7;

//int motor4_Speed=;
//int motor4_B=;
//int motor4_A=;

int motor2_A=6;
int motor2_B=5;
int motor2_Speed=3;

char number[50]; //ka wieso^^

void receiveData(int byteCount) {
  while (Wire.available()) {
    int number = Wire.read();
    if (number == 1){    //vorne
     Fahren();  
     }
    if (number == 2){
    Rechts();
    }
    if (number == 3){   //links
    //digitalWrite(4, HIGH);
     Links();
    }
    if (number == 4){  //hinten
    //digitalWrite(2, HIGH);
   // Serial.print (number);
   Hinten();
    }
    if (number == 5){   //keininput
      Stop();
     
    }
  }
   
 }
void Fahren(){   
   digitalWrite(motor1_A,HIGH); 
   digitalWrite(motor1_B,LOW);
   digitalWrite(motor2_A,LOW); 
   digitalWrite(motor2_B,HIGH);
   analogWrite(motor1_Speed,255);
   analogWrite(motor2_Speed,255);
  }
void Rechts(){ 
    analogWrite(motor1_Speed,255);
    analogWrite(motor2_Speed,255);
    digitalWrite(motor1_A,HIGH); 
    digitalWrite(motor1_B,LOW);
    digitalWrite(motor2_A,HIGH); 
    digitalWrite(motor2_B,LOW);
}
void Hinten(){
  analogWrite(motor1_Speed,255);
  analogWrite(motor2_Speed,255);
  digitalWrite(motor1_A,LOW);
  digitalWrite(motor1_B,HIGH);
  digitalWrite(motor2_A,HIGH);
  digitalWrite(motor2_B,LOW);
}

void Links(){ 
   analogWrite(motor1_Speed,255);
  analogWrite(motor2_Speed,255);
  digitalWrite(motor1_A,LOW);
  digitalWrite(motor1_B,HIGH);
  digitalWrite(motor2_A,LOW);
  digitalWrite(motor2_B,HIGH);
}
void Stop(){
  analogWrite(motor1_Speed,0);
  analogWrite(motor2_Speed,0);
  digitalWrite(motor1_A,LOW);
  digitalWrite(motor1_B,LOW);
  digitalWrite(motor2_A,LOW);
  digitalWrite(motor2_B,LOW);
}
void setup(){
  Serial.begin(9600);
  Serial.setTimeout(500);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  pinMode(motor1_A,OUTPUT);
  pinMode(motor1_B,OUTPUT);
  pinMode(motor2_A,OUTPUT);
  pinMode(motor2_B,OUTPUT);
  Serial.begin (9600);
 }


void loop() {
  // delay(100);
    //Hinten();
    //Stop();



}

