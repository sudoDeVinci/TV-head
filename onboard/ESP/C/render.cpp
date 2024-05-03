#include "render.h"

/**
 * Read the integer value from a conf file line.
 */
int readConfInt(String line) {
  return line.substring(line.indexOf('=') + 1).toInt();
}

/**
 * Read the float value from a conf file line. 
 */
float readConfFloat(String line) {
  return line.substring(line.indexOf('=') + 1).toFloat();
}

/**
 * Read settings from SD card and populate renderer struct. 
 */
void readSettingsConf(fs::FS &fs, const char *path, Renderer *renderer) {
  String pathStr = String(CONFIG_FOLDER) + "/" + String(path);
  File file  = fs.open(pathStr.c_str());
  if (!file) {
    debugln("Failed to open config file.");
    return;
  }

  while (file.available()) {
    String line = file.readStringUntil('\n');
    line.trim();

    if (line.startsWith("LEDS")) {
      renderer -> LEDS = readConfInt(line);
    
    } else if (line.startsWith("PIN")) {
      renderer -> PIN = readConfInt(line);
    
    } else if (line.startsWith("CHANNEL")) {
      renderer -> CHANNEL = readConfInt(line);
    
    } else if (line.startsWith("SPEED")) {
      renderer -> SPEED = readConfInt(line);

    } else if (line.startsWith("BRIGHTNESS")) {
      renderer -> BRIGHTNESS = readConfFloat(line);
    }
  }

  // Print config to make sure it's all good.
  renderer -> print();
}