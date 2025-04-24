#include <M5Atom.h>
#include <WiFi.h>

// Create your SoftAP name (SSID) and password
const char *ssid = "M5ATOM_SoftAP";
const char *password = "12345678";

void setup() {
M5.begin(true, true, true);  // Initialize Atom Matrix
  M5.dis.clear(); // Clear every led (including memory)
  Serial.begin(115200);
  delay(1000);

  // Start SoftAP
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.println("SoftAP started.");
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

void loop() {

}
