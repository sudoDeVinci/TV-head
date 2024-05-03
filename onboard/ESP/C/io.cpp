#include "io.h"

String HEADERS[] = {"index","blue","green","red"};

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
  if (!file || !file.available()) return false;
  String line = "";
  while ((line = file.readStringUntil('\n')) && !line.startsWith(HEADERS[0])) {
    // Read lines until a line starts with the expected header
  }

  int HEADERS_SIZE = sizeof(HEADERS) / sizeof(HEADERS[0]);
  String* header_values = new String[HEADERS_SIZE];
  int header_index = 0;
  int pos = 0;
  int commaIndex = 0;
  
  // Extract values from the header line
  while ((pos = line.indexOf(',', commaIndex)) != -1 && header_index < HEADERS_SIZE) {
    header_values[header_index++] = line.substring(commaIndex, pos);
    commaIndex = pos + 1;
  }
  header_values[header_index++] = line.substring(commaIndex); // Last value after last comma
  
  // Check if the number of values in the header line matches the expected number
  if (header_index != HEADERS_SIZE) {
    debugln("Invalid frame header: incorrect number of values");
    return false;
  }

  return true;
}



/**
 * Get the animation paths.
 */
std::vector<String> getAnimationPaths(fs::FS &fs) {
  std::vector<String> paths;
  
  File dir = fs.open(ANIMATION_FOLDER);
  if (!dir || !dir.isDirectory()) {
    debugln("Failed to open animation folder");
    return paths;
  }
  
  while (File entry = dir.openNextFile()) {
    if (entry.isDirectory()) {
      // Check if directory is not root and add to paths
      if (strcmp(entry.name(), "/") != 0) {
        paths.push_back(entry.name());
      }
    }
    entry.close();
  }
  
  dir.close();
  
  return paths;
}

/**
 * Read a single frame from a csv file.
 */
std::vector<std::array<uint16_t,4>> readFrame(File file) {
  std::vector<std::array<uint16_t, 4>> frame;

  while (file.available()) {
    String line = file.readStringUntil('\n');
    uint16_t index, r, g, b;
    sscanf(line.c_str(), "%d,%d,%d,%d", &index, &r, &g, &b);
    frame.push_back({index, r, g, b});
  }

  return frame;
}


/**
 * Read frames from CSV files in a folder and return them as a list of frames
 */
std::vector<std::vector<std::array<uint16_t, 4>>> readFrames(fs::FS &fs, const char* folderPath) {
    std::vector<std::vector<std::array<uint16_t, 4>>> frames;

    File dir = fs.open(folderPath);

    if (!dir || !dir.isDirectory()) {
    debugln("Failed to open animation folder");
    return frames;
    }
  
    while (File file = dir.openNextFile()) {
        if (file.isDirectory()) continue;

        if (!String(file.name()).endsWith(".csv")) {
          file.close();
        }
        
        if(!validHeader(file)) {
          file.close();
          continue;
        }

        frames.push_back(readFrame(file));   

        file.close();
    }

    dir.close();
    return frames;
}