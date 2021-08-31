#include <LWiFi.h>
#include <TLSClient.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <WiFiUdp.h>
#include <math.h>

#define LIGHT_SENSOR A0//Grove - Light Sensor is connected to A0 of Arduino
const int ledPin=7;                 //Connect the LED Grove module to Pin7, Digital 7
const int thresholdvalue=2000;         //The treshold for which the LED should turn on. Setting it lower will make it go on at more light, higher for more darkness
float t, Rsensor; //Resistance of sensor in K


const char* ssid =  "Linkit_ASUS";   // name of your WiFi network
const char* pass =  "12345678"; // password of the WiFi network
int status = WL_IDLE_STATUS;

void setup() 
{
    Serial.begin(9600);                //Start the Serial connection
    pinMode(ledPin,OUTPUT);            //Set the LED on Digital 7 as an OUTPUT
    pinMode(LED_BUILTIN, OUTPUT);
    
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    // attempt to connect to Wifi network:
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
        status = WiFi.begin(ssid, pass);
    }
    Serial.println("Connected to wifi");
    printWifiStatus();

}
void loop() 
{
    float sensorValue = analogRead(LIGHT_SENSOR); 
    Rsensor = (float)(4095-sensorValue)*10/sensorValue;
    t = (sensorValue/Rsensor)/10;

    Serial.println("");
    Serial.println("Analog Data :");
    Serial.println(sensorValue);
    Serial.println("Sensor resistance:");
    Serial.println(Rsensor,DEC);//show the ligth intensity on the serial monitor;
    Serial.println("Read :");
    Serial.println(t);
    Serial.println("");

    if (sensorValue < 2000)
    {
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100); 
    }
    else
    {
      digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
      delay(100); 
    }
    delay(2500);
}

void printWifiStatus() {
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print your WiFi shield's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}
