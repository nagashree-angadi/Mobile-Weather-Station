#include <SD.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <String.h>
#include <dht.h>
 
SoftwareSerial mySerial(7, 8);

dht DHT;
TinyGPS gps; 
File logFile;

#define DHT11_PIN 31

long Latitude,Longitude; 
int AQ135_Sense = A0; 
int CO_Sense = A1; 
int Temperature,Humidity,AirQ,CO;

byte buff[2];
int pin = 2;//DSM501A input D2
unsigned long duration;
unsigned long starttime;
unsigned long endtime;
unsigned long sampletime_ms = 30000;
unsigned long lowpulseoccupancy = 0;
double ratio = 0;
double concentration = 0;
double concentration_up;
double CO_updated;
int i=0;

void setup()
{              
  Serial.begin(9600); 
  Serial3.begin(9600);
  mySerial.begin(9600);
  Serial.print("Initializing SD card...");
  pinMode(53, OUTPUT);

  if (!SD.begin(53)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");     
  delay(1000);
  pinMode(2,INPUT);
  starttime = millis(); 
}
 
void loop()
{
  delay(5000);delay(5000);
  int chk = DHT.read11(DHT11_PIN);
  Temperature = DHT.temperature;  
  Humidity = DHT.humidity;
  delay(5000);delay(5000);
  AirQ = analogRead(AQ135_Sense); 
  CO = analogRead(CO_Sense);
 
  duration = pulseIn(pin, LOW);
  lowpulseoccupancy += duration;
  endtime = millis();
  if ((endtime-starttime) > sampletime_ms)
  {
    ratio = (lowpulseoccupancy-endtime+starttime + sampletime_ms)/(sampletime_ms*10.0);  
    concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; 
    lowpulseoccupancy = 0;
    starttime = millis();
  } 
  concentration_up = concentration/10;
  CO_updated = CO/100.0;
 
  Serial.print("Temperature :");
  Serial.println(Temperature);
     
  Serial.print("Humidity :");
  Serial.println(Humidity);
     
  Serial.print("CO :");
  Serial.println(CO_updated);
      
  Serial.print("Dust :");
  Serial.println(concentration_up,5); 
    
  for(unsigned int c=0;c<=60000;c++)
  {
    while(Serial3.available()){ 
    if(gps.encode(Serial3.read())){ 
      gps.get_position(&Latitude,&Longitude); 
    
      Serial.println("Position: ");
      Serial.print("lat: ");Serial.print(Latitude);Serial.print(" ");
      Serial.print("lon: ");Serial.println(Longitude);
      }
    }
  }

   logFile = SD.open("datalog.txt", O_WRITE | O_CREAT | O_TRUNC);
   if (logFile) {
    Serial.println("Writing to datalog.txt...");
    logFile.println(Temperature,DEC);
    logFile.println(Humidity,DEC);
    logFile.println(CO_updated,DEC);
    logFile.println(concentration_up,5);
    logFile.println(Latitude);
    logFile.println(Longitude);
    logFile.close(); 
    Serial.println("done.");
    } else {
    Serial.println("error opening datalog.txt");
    } 

  logFile = SD.open("datalog.txt");
  if (logFile) {
  Serial.println("Reading from datalog.txt...");
  while (logFile.available()) {
  Serial.write(logFile.read());
  }
  logFile.close();
  } else {
  Serial.println("error opening test.txt");
  } 
     
  //delay(200);          
  Send2Cloud();
  
  if (mySerial.available())
    Serial.write(mySerial.read());
}

void Send2Cloud()
{
  mySerial.println("AT");
  delay(1000);

  mySerial.println("AT+CPIN?");
  delay(1000);

  mySerial.println("AT+CREG?");
  delay(1000);

  mySerial.println("AT+CGATT?");
  delay(1000);

  mySerial.println("AT+CIPSHUT");
  delay(1000);

  mySerial.println("AT+CIPSTATUS");
  delay(2000);

  mySerial.println("AT+CIPMUX=0");
  delay(2000);
 
  ShowSerialData();
              
  mySerial.println("AT+CSTT=\"airtelgprs.com\"");
  delay(1000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIICR");
  delay(3000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIFSR");
  delay(2000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSPRT=0");
  delay(3000);
 
  ShowSerialData();
  
  mySerial.println("AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"");
  delay(6000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSEND");
  delay(4000);
  ShowSerialData();
  
  String str="GET https://api.thingspeak.com/update?api_key=K5O1L96CHUAAFAQA&field1="+String(CO_updated)+String("&field2=")+String(concentration)+String("&field3=")+String(Humidity)+String("&field4=")+String(Temperature)+String("&field5=")+String(Latitude)+String("&field6=")+String(Longitude);
  mySerial.println(str);
  delay(4000);
  ShowSerialData();
  Serial.println("Data sent to cloud");
  
  mySerial.println((char)26);
  delay(5000); 
  mySerial.println();
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSHUT");
  delay(100);
  ShowSerialData();
} 

void ShowSerialData()
{
  while(mySerial.available()!=0)
    Serial.write(mySerial.read());
}
