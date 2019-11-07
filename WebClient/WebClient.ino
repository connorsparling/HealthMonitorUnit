/* Web Client */

#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = "9 Coup Idiot Show";
char pass[] = "9guys1house";

int status = WL_IDLE_STATUS;

char server[] = "192.168.2.97";
int PORT = 8080;

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial){
    // wait for the serial port to connect
  }
  Serial.println("aahhhhh");
  delay(3000);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(5000);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();

  delay(10000);
  

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(server, PORT)) {
    Serial.println("connected to server");
    // Make a HTTP request:
    client.println("POST /search?q=arduino HTTP/1.1");
    client.println("Host: 192.168.2.97");
    client.println("Connection: close");
    client.println();
  }
  
  delay(10000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Done Program");

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
