#include <M5Atom.h>

// This function displays a number from 0 to 5 in the M5 Atom Matrix led screen
// The color of the number is either red if tag (0) or green if anchor (1)
int deviceMode = 0;  // 0 = Tag, 1 = Anchor
int deviceID = 1;    // Device id

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
    M5.begin(true, false, true);  // Begin M5Atom Matrix
    M5.dis.clear(); // Clear every led (including memory)

    uint32_t color = (deviceMode == 0) ? 0x00FF00 : 0xFF0000;  // Green for tags, red for anchors

    showNumber(deviceID, color);
}

void loop() {}
