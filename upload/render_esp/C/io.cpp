#include "io.h"

/**
 * Initialize the sdcard file system. 
 */
void sdmmcInit(void){
  SD_MMC.setPins(SD_MMC_CLK, SD_MMC_CMD, SD_MMC_D0);
  if (!SD_MMC.begin("/sdcard", true, true, SDMMC_FREQ_DEFAULT, 5)) {
    debugln("Card Mount Failed");
    return;
  }
  uint8_t cardType = SD_MMC.cardType();
  if(cardType == CARD_NONE){
      debugln("No SD_MMC card attached");
      return;
  }

  uint64_t cardSize = SD_MMC.cardSize() / (1024 * 1024);
  debugf("SD_MMC Card Size: %lluMB\n", cardSize);  
  debugf("Total space: %lluMB\r\n", SD_MMC.totalBytes() / (1024 * 1024));
  debugf("Used space: %lluMB\r\n", SD_MMC.usedBytes() / (1024 * 1024));
}

/**
 * Check if the file header is valid. 
 */
bool validHeader(File file) {
  if (!file.available()) return false;
  String line = "";
  while (file.available() || !line.startswith(HEADERS[0])) {
    line = file.readStringUntil('\n');
  }

  String[] header_values = line.split(",");
  if (header_values.length!= HEADERS.length) {
    debugln("Invalid frame header");
    return false;
  }

  for (int i = 0; i < HEADERS.length; i++) {
    if (header_values[i]!= HEADERS[i]) {
      debugln("Invalid frame header");
      return false;
    }
  }
  return true;
}


/**
 * Get the animation paths.
*/
String* getAnimationPaths(fs::FS &fs, const char* folderPath = ANIMATION_FOLDER) {
  String paths = "";
  
  File dir = fs.open(folderPath);
  if (!dir || !dir.isDirectory()) {
    Serial.println("Failed to open animation folder");
    return paths;
  }
  
  while (File entry = dir.openNextFile()) {
    if (entry.isDirectory()) {
      // Check if directory is not root and add to paths
      if (strcmp(entry.name(), "/") != 0) {
        paths += entry.name();
        paths += "\n";
      }
    }
    entry.close();
  }
  
  dir.close();
  
  return paths.split("\n");
}


/**
 * read frames from CSV files in a folder and return them as a list of frames
 */
std::vector<std::array<int, 4>> readFrames(const char* folderPath) {
    std::vector<std::array<int, 4>> frames;
    File dir = fs.open(folderPath);

    if (!dir || !dir.isDirectory()) {
    Serial.println("Failed to open animation folder");
    return frames;
    }
  
    while (File file = dir.openNextFile()) {
        if (file.isDirectory()) continue;

        if (!String(file.name()).endsWith(".csv")) continue;

        debugf("Reading frames from: %s\n", file.name());
        
        if(!validHeader(file)) continue;

        while (file.available()) {
            String line = file.readStringUntil('\n');
            int index, r, g, b;
            sscanf(line.c_str(), "%d,%d,%d,%d", &index, &r, &g, &b);
            frames.push_back({index, r, g, b});
        }   

        file.close();
    }

    dir.close();
    return frames;
}

String free_mem(bool full = false) {
  uint32_t F = ESP.getFreeHeap();
  uint32_t T = ESP.getHeapSize();
  uint32_t P = F * 100 / T;
  String result;
  
  if (!full) {
    result = "FREE: " + String(P, 4) + "%";
  } else {
    uint32_t A = T - F;
    result = "Total:" + String(T) + " Free:" + String(F) + " (" + String(P, 4) + "%)";
  }
  
  return result;
}