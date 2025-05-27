#include <M5Atom.h>
#include <WiFi.h>

#include "config.h"

#define UWB_RX 32  // RX in the Atom Matrix (connect to TX in the UWB module)
#define UWB_TX 26  // TX in the Atom Matrix (connect to RX in the UWB module)

int TAG_ID = 1;   // The id that the tag will have

WiFiClient client; // WiFi object

// Function that displays tag
void showNumber(int num, uint32_t color) {
    const uint8_t numbers[10][5][5] = {
        {{0,0,1,0,0}, {0,1,0,1,0}, {0,1,0,1,0}, {0,1,0,1,0}, {0,0,1,0,0}},  // 0
        {{0,0,1,0,0}, {0,1,1,0,0}, {0,0,1,0,0}, {0,0,1,0,0}, {0,1,1,1,0}},  // 1
        {{0,1,1,0,0}, {0,0,0,1,0}, {0,0,1,1,0}, {0,1,0,0,0}, {0,1,1,1,0}},  // 2
        {{0,1,1,1,0}, {0,0,0,1,0}, {0,1,1,1,0}, {0,0,0,1,0}, {0,1,1,1,0}},  // 3
        {{0,1,0,1,0}, {0,1,0,1,0}, {0,1,1,1,0}, {0,0,0,1,0}, {0,0,0,1,0}},  // 4
        {{0,1,1,1,0}, {0,1,0,0,0}, {0,1,1,1,0}, {0,0,0,1,0}, {0,1,1,0,0}}  // 5
    };

    M5.dis.fillpix(0x000000);  // Turn off every led

    for (int y = 0; y < 5; y++) {
        for (int x = 0; x < 5; x++) {
            if (numbers[num][y][x]) {
                M5.dis.drawpix(y * 5 + x, color);  // Turn on pixels
            }
        }
    }
}

void setup() {
  M5.begin(true, true, true);  // Initialize Atom Matrix (serial, I2C, Display)
  M5.dis.clear(); // Clear every led (including memory)
  Serial.begin(115200);         // Serial to PC
  Serial2.begin(115200, SERIAL_8N1, UWB_RX, UWB_TX);  // Serial to UWB

  delay(100);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); 
    Serial.print("."); // Prints a dot until it succeeds
  }
  Serial.println("\nWiFi connected");

  // Open a TCP connection to the given host and port. Tries until succees
  while (!client.connect(host, port)) {
    Serial.println("Connection to TCP server failed. Retrying...");
    delay(2000);
  }
  Serial.println("Connected to server!");

  Serial.println("Initializing UWB...");

  Serial2.print("AT+RST\r\n"); // Reset module
  delay(100);

  // Verify communication with UWB module
  Serial2.print("AT+version?\r\n"); // Get manufacturer, module series and version number
  delay(200);
  if (Serial2.available()) {
      String version = Serial2.readString();
      Serial.println("UWB version: " + version);
  }
  delay(100);

  Serial.println("Setting UWB as tag...");
  // Config UWB module as tag
  for (int b = 0; b < 2; b++) { // Two times according to documentation
    // Serial.println("Setting AT+anchor_tag:");
    delay(100);
    Serial2.print("AT+anchor_tag=0,");  // Set tag mode
    Serial2.print(TAG_ID);        // Set tag
    Serial2.print("\r\n");
    // Serial.println("Setting AT+interval:");
    delay(100);
    Serial2.print("AT+interval=5\r\n");    // Set distance measurement interval - update rate (between 5-50 meters)
    // Serial.println("AT+switchdis:");
    delay(100);
    Serial2.print("AT+switchdis=1\r\n");    // Switch to control whether to range or not, valid only in tag mode
    delay(100);
    if (b == 0) {
        Serial2.print("AT+RST\r\n"); // Reset
      }
  }

  delay(50);
  Serial.print("Tag set");

  showNumber(TAG_ID, 0x00FF00); // Show in the screen the id in green

}

void loop() {
  // Optimized data reading
  while (Serial2.available()) { // Use while instead of if
    String uwbData = Serial2.readStringUntil('\n');  // Read line-by-line
    Serial.println(uwbData); // Send data to PC via Serial

    if (client.connected()) {
      client.println(uwbData); // Send data to PC via TCP
    }
  }
}
