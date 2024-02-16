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
 * Get the line count of a file 
 */
int getLineCount(fs::FS &fs, const char *filename) {
  File file = fs.open(filename);
  if (!file) {
    debugln("Failed to open Server config file");
    return -1;
  }

  int count = 0;
  while (file.available()) {
    file.readStringUntil('\n');
    count++;
  }

  return count;
}



/**
 * Create a a new directory structure.
*/
void createDir(fs::FS &fs, const char * path){
    Serial.printf("Creating Dir: %s\n", path);
    if(fs.mkdir(path)){
        Serial.println("Dir created");
    } else {
        Serial.println("mkdir failed");
    }
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
 * Get the number of files with the specified extension.
 */
int getFileCount(fs::FS &fs, const char* root, const char* extension) {
  File dir = fs.open(root);

  if(!root){
    debugln("Failed to open directory");
    return -1;
  }

  if(!root.isDirectory()){
      debugln("Not a directory");
      return -1;
  }

  int count = 0;
  File file = root.openNextFile();
  while(file) {
    if(file.isFile() && String(file.name).endsWith(extension)){
        debug("  FILE : ");
        debugln(file.name());
        count++;
    }
  }
  dir.close()
  return count;
}


/**
 * List the files with the specified extension. 
 */
char* listFiles(fs::FS &fs, const char* root, const char* extension, char* fileList) {
  File directory = fs.open(root);
  if(!root){
      debugln("Failed to open directory");
      return;
  }

  File dir = fs.open(root);

  if(!root){
    debugln("Failed to open directory");
    return;
  }

  if(!root.isDirectory()){
      debugln("Not a directory");
      return;
  }

  int index = 0;
  File file = root.openNextFile();
  while(file) {
    if(file.isFile() && String(file.name).endsWith(extension)){
      fileList[index] = file.name();
    }
  }
}


/**
 * Read a csv frame from the SD card 
 */
void loadFrame(File file, const char *filename, int[][] frame, int frame_length) {
  // read the first line, split it, and check it against the headers
  if (!validHeader(file, frame)) {
    debugln("Invalid frame header");
    return;
  }
  
  // decrement to account for header.
  int line_count = frame_length;
  int included = 0;

  /*
   * Read the line, split it, then check the number of values.
   * Once confirmed, convert each value to integer, and put into the frame.
   */
  while (file.available()) {
    String line = file.readStringUntil('\n');
    //check if line is empty
    if (line.length() == 0) continue;
    
    String[] values = line.split(",");
    if (values.length!= headers.length) {
      debug("Invalid frame line definition : ");
      for(int i = 0; i < values.length < i++) debug(String(values[i]) + ", ");
      debugln("");
      return;
    }

    for (int i = 0; i < values.length; i++) {
      int value = values[i].toInt();
      frame[included][i] = value;
    }

    included++;
  }
}

void idkyet(fs::FS &fs, const char* root) {
  int fileCount = getFileCount(fs, root, extension);
  if (fileCount == -1) return nullptr;
  char* fileList = new char[fileCount];
}