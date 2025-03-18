#include <M5Atom.h>

#define UWB_RX 32  // RX in the Atom Matrix (connect to TX in the UWB module)
#define UWB_TX 26  // TX in the Atom Matrix (connect to RX in the UWB module)

int ANCHOR_ID = 3; // The id that the anchor will have

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
  M5.begin(true, true, true);  // Initialize Atom Matrix
  M5.dis.clear(); // Clear every led (including memory)
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

  for (int b = 0; b < 2; b++) { // Two times according to documentation
    delay(50);
    //Serial2.print("AT+anchor_tag=1,0\r\n"); // Anchor mode, id = 0
    Serial2.print("AT+anchor_tag=1,");  // Set anchor mode
    Serial2.print(ANCHOR_ID);        // Set anchor id
    Serial2.print("\r\n");
    delay(1);
    delay(50);
    if (b == 0) {
      Serial2.print("AT+RST\r\n"); //Reset
    }
  }

  delay(50);
  Serial.println("Anchor set");

  showNumber(ANCHOR_ID, 0xFF0000); // Show in the screen the id in red

}

void loop() {
}
