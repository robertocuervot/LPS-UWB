#include <M5Atom.h>

#define UWB_RX 32  // RX in the Atom Matrix (connect to TX in the UWB module)
#define UWB_TX 26  // TX in the Atom Matrix (connect to RX in the UWB module)

String DATA  = "";  // Used to store distance data
int UWB_MODE = 0;   // Used to set UWB mode: 0 -> Tag, 1 -> Anchor


void setup() {
  M5.begin(true, true, true);  // Initialize Atom Matrix
  Serial.begin(115200);         // Serial to PC
  Serial2.begin(115200, SERIAL_8N1, UWB_RX, UWB_TX);  // Serial to UWB

  delay(100);

  Serial.println("Initializing UWB...");

  Serial2.print("AT+RST\r\n");          // Reset module
  delay(1000);

  // Verify communication with UWB module
  Serial2.print("AT+version?\r\n"); // Get manufacturer, module series and version number
  delay(200);
  if (Serial2.available()) {
      String version = Serial2.readString();
      Serial.println("UWB version: " + version);
  }
  delay(1000);

  Serial.println("Setting module UWB as ANCHOR...");

  Serial2.print("AT+RST\r\n");          // Reset
  delay(1000);
  Serial2.print("AT+anchor_tag=1,0\r\n"); // Anchor mode, id = 0
  delay(500);

  Serial.println("Anchor set");

}

void loop() {
}
