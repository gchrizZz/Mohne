#include <Servo.h>
// include the library code
#include <LiquidCrystal.h>
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// initialize our variables
int inches = 0;

int cm = 0;

int pos = 0;

int sensorPin = 0;

long readUltrasonicDistance(int pin)
{
  pinMode(pin, OUTPUT);  // Clear the trigger
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  // Sets the pin on HIGH state for 10 micro seconds
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin, LOW);
  pinMode(pin, INPUT);
  // Reads the pin, and returns the sound wave travel time in microseconds
  return pulseIn(pin, HIGH);
}

Servo servo_9;

void setup()
{
  pinMode(7, INPUT);
  Serial.begin(9600);

  servo_9.attach(9);
 // set up the LCD's number of columns and rows:  
  lcd.begin(16, 2); 
  
}

void loop()
{
  // measure the ping time in cm
  cm = 0.01723 * readUltrasonicDistance(7);
  // convert to inches by dividing by 2.54
  inches = (cm / 2.54);
  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.println("cm");
  delay(100); // Wait for 100 millisecond(s)
  if (cm < 50) {
    servo_9.write(180);}
    else {
    servo_9.write(0);
      
lcd.clear();
int reading = analogRead(sensorPin); 
// convert the reading to a voltage
float voltage = reading * 5.0;
voltage /= 1024.0; 
// convert the voltage to a temperature
float temperatureC = (voltage - 0.5) * 100 ; 
lcd.print(temperatureC); lcd.println(" degrees C ");
delay(1000);
  
  }
}