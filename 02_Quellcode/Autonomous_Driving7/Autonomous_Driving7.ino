//Libraries
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//Ultrasonic sensor pins
#define trigPinL 13
#define echoPinL 12
#define trigPinR 2 //vorher A3
#define echoPinR 3
#define trigPinM 10 //vorher A1
#define echoPinM 4 //vorher A2

//Motor pins
#define ENL 5
#define ENR 6
#define IN1 7
#define IN2 8
#define IN3 9
#define IN4 11

//IR sensors pins only for digital use
#define sensorValueR A1
#define sensorValueM A2
#define sensorValueL A3
long sensors_average;
int sensors_sum;
int posi;
int IRSensor[3]={0, 0, 0};

//Display
#define OLED_RESET 0
Adafruit_SSD1306 display(OLED_RESET);

void setup() {
  Serial.begin (9600);
// setup ultrasonic sensors
  pinMode(trigPinL, OUTPUT);
  pinMode(echoPinL, INPUT);
  pinMode(trigPinR, OUTPUT);
  pinMode(echoPinR, INPUT);
  pinMode(trigPinM, OUTPUT);
  pinMode(echoPinM, INPUT);
//setup ir sensors only for digital use
  //pinMode(sensorValueL,INPUT);
  //pinMode(sensorValueR,INPUT);
  //pinMode(sensorValueM,INPUT);
//setup display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); //initialize with the I2C addr 0x3C (128x64)
  display.clearDisplay();
//setup motors 
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
//setup "speedPins"
  pinMode(ENL, OUTPUT);
  pinMode(ENR, OUTPUT);
}

//MotorSpeed should be at least 100
int max_speed = 120;
int motorSpeedL = 0;
int motorSpeedR = 0;

//initialize distance with 0
int distanceL = 0, distanceR = 0, distanceM = 0;

//initializse PID variables
float  proportional=0.0;
float  integral=0.0;
float  derivative=0.0;
float  Kp=150.0;
float  Ki=0.15;
float  Kd=100.0;
float  error_value=0.0;
float  last_proportional=0.0;

//initialize ir sensor values
int irthreshold = 220;
int irthresholdR = 630;// extra Schwellle für rechten Sensor, da der anscheinend defekt ist und Schmarrn misst.
int irthresholdL = 615;// extra Schwellle für rechten Sensor (in zusammenhang mit linkem Sensor), da der anscheinend defekt ist und Schmarrn misst.

//forward
void forward(){ 
  analogWrite(ENL, motorSpeedL+110);
  analogWrite(ENR, motorSpeedR+110);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("Forward");//debug
}

//back
void back() {
  analogWrite(ENL, motorSpeedL+130);
  analogWrite(ENR, motorSpeedR+130);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("Back");
}

//left
void left() {
  analogWrite(ENL, motorSpeedL+150);
  analogWrite(ENR, motorSpeedR+30);
  digitalWrite(IN1, HIGH);//
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);//
  digitalWrite(IN4, HIGH);
  Serial.println("Left"); //debug
}

//right
void right() {
  analogWrite(ENL, motorSpeedL+30);
  analogWrite(ENR, motorSpeedR+150);
  digitalWrite(IN1, HIGH);//
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);//
  digitalWrite(IN4, HIGH);
  Serial.println("Right");//debug
}

//Pointturn left
  void PTleft() {
  analogWrite(ENL, motorSpeedL+180);
  analogWrite(ENR, motorSpeedR+180);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("PTLeft"); //debug
}

// Pointturn right
void PTright() {
  analogWrite(ENL, motorSpeedL+180);
  analogWrite(ENR, motorSpeedR+180);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("PTRight");//debug
}

//stop
void stop() {
  digitalWrite(ENL, LOW);
  digitalWrite(ENR, LOW);
  Serial.println("Stop!");//debug
} 

//Ultrasonic distance measurement functions 
int distance_measureL(){
  float durationL, distanceL; 
  digitalWrite(trigPinL, LOW);
  delayMicroseconds(2); 
  digitalWrite(trigPinL, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPinL, LOW);
  durationL = pulseIn(echoPinL, HIGH);
  distanceL = (durationL/2) / 29.1;
    return (int)distanceL;
  }
  
int distance_measureR(){
  float durationR, distanceR;  
  digitalWrite(trigPinR, LOW);
  delayMicroseconds(2); 
  digitalWrite(trigPinR, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPinR, LOW);
  durationR = pulseIn(echoPinR, HIGH);
  distanceR = (durationR/2) / 29.1; 
  return (int)distanceR;
  }

int distance_measureM(){
  float durationM, distanceM;  
  digitalWrite(trigPinM, LOW);
  delayMicroseconds(2); 
  digitalWrite(trigPinM, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPinM, LOW);
  durationM = pulseIn(echoPinM, HIGH); 
  distanceM = (durationM/2) / 29.1;  
  return (int)distanceM;
  }

//sensor read
void readIRSsensors()
{
sensors_average = 0;
sensors_sum = 0; 
for (int i = 0; i < 3; i++){
IRSensor[i] = analogRead(i);
sensors_average += IRSensor[i] * i * 1000;   
sensors_sum += int(IRSensor[i]);}
posi = int(sensors_average / sensors_sum);
/*
Serial.print(sensors_average);
Serial.print(" sensors_average ");
Serial.print(sensors_sum);
Serial.print(" sensors_sum ");
Serial.print(posi);
Serial.print(" posi ");
Serial.println();
//delay(1000);
*/
}

//PID calculation, for better motorcontrol
void calculatePID()
{
posi = int(sensors_average / sensors_sum);
proportional = float(posi - 11);
integral = (integral + proportional);
derivative = proportional - last_proportional;
last_proportional = proportional;
error_value = int(proportional * Kp + integral * Ki + derivative * Kd);

/*Serial.print(posi);
Serial.print(" posi ");
Serial.print(proportional);
Serial.print(" proportional ");
Serial.print(integral);
Serial.print(" integral ");
Serial.println();
Serial.print(derivative);
Serial.print(" derivative ");
Serial.print(last_proportional);
Serial.print(" last_proportional ");
Serial.println();
Serial.print(error_value);
Serial.print(" error_value ");
Serial.println();
//delay(2000);
*/
}

//calculate motorturns
void motorturn(){  //Restricting the error value between +255.
if (error_value< -120){ error_value = -120;     } if (error_value> 120){
error_value = 120;
    }
 
// If error_value is less than zero calculate right turn speed values
if (error_value< 0){
motorSpeedR = max_speed + error_value;
motorSpeedL = max_speed;
Serial.println("Right"); //debug
    }
 
// Iferror_value is greater than zero calculate left turn values
 
else{
motorSpeedR = max_speed;
motorSpeedL = max_speed - error_value;
Serial.println("Left"); //debug
    }
}

//PID controled motorspeed
void motor_drive(int motorSpeedR,int motorSpeedL){
analogWrite(ENR, motorSpeedR);
analogWrite(ENL, motorSpeedL);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

//////////////////////////////////////////////Mainloop//////////////////////////////////////////////////////
void loop() {
//Write distances into their variables, by getting them from the function
distanceL = distance_measureL();
distanceR = distance_measureR();
distanceM = distance_measureM();
  
//Initialize Display, by cleaning it up
    display.clearDisplay();
    
//Show dinstanceL = left ultrasonic sensor  
    display.setCursor(25,5);
    display.setTextSize(2);
    display.setTextColor(WHITE);
    display.println(distanceL);
    display.setCursor(60,5);
    display.println("cm");
    display.setCursor(5,5);
    display.println("L");
    display.display();
    
//Show distanceR = right ultrasonic sensor
    display.setCursor(25,25);
    display.println(distanceR);
    display.setCursor(60,25);
    display.println("cm");
    display.setCursor(5,25);
    display.println("R");
    display.display();

//Show distanceM = middle ultrasonic sensor
    display.setCursor(25,45);
    display.println(distanceM);
    display.setCursor(60,45);
    display.println("cm");
    display.setCursor(5,45);
    display.println("M");
    display.display();
/*
//Show ir sensors on oled
  if((digitalRead(sensorValueR))==LOW){
    display.setTextSize(2);
    display.setTextColor(WHITE);
    display.setCursor(85,5);
    display.println("IRL");
    display.display();
    Serial.println(sensorValueR);
  }
    //mit analog werten if((irthresholdL<IRSensor[0])&& (irthreshold<IRSensor[0])&&(IRSensor[0]<irthresholdR)){
    if((digitalRead(sensorValueL))==LOW){
    display.setTextSize(2);
    display.setTextColor(WHITE);
    display.setCursor(85,25);
    display.println("IRR");
    display.display();
    Serial.println(sensorValueL);
  }
    if((digitalRead(sensorValueM))==LOW){
    display.setTextSize(2);
    display.setTextColor(WHITE);
    display.setCursor(85,45);
    display.println("IRM");
    display.display();
    Serial.println(sensorValueM);
  }
  */
//here starts the magic ;-)
//on the line
/*if ((((digitalRead(sensorValueR))==HIGH) || ((digitalRead(sensorValueL))==HIGH) || ((digitalRead(sensorValueL))==HIGH)) && ((distance_measureL()>25 || distance_measureR()>15 || distance_measureM>12))){
  readIRSsensors();
  calculatePID();    
  motorturn();
  motor_drive(motorSpeedR,motorSpeedL);
}
else if (distance_measureL()<8 || distance_measureR()<8 || distance_measureM()<10)
      {
      stop();
      if (distance_measureL() > distance_measureR())
      PTleft();
      if (distance_measureL() < distance_measureR())
      PTright();
      } 
      */ 
//beside the line
if (distanceL>15 && distanceR>12 && distanceM>10){
forward();
}
if (distanceL<15 && distanceR>12 && distanceM>10){
left();
}
if (distanceL>15 && distanceR<12 && distanceM>10){
right();
}
//Emergencystop beside the line
if (distanceL<10 || distanceR<10 || distanceM<10)     
      {
      stop();
      delay(50);
      if (distanceL > distanceR)
      PTleft();
      delay(150);
      if (distanceL < distanceR)
      PTright();
      delay(150);
      }
if (distanceL<5 || distanceR<5 || distanceM<5)      
      {
      stop();
      back();
      delay (50);
      }  
}

