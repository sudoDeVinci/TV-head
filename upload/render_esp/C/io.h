#pragma once
#ifndef IO_H
#define IO_H

#include <Arduino.h>
#include "FS.h"
#include "SD_MMC.h"

#define DEBUG 1

#if DEBUG == 1
#define debug(...) Serial.print(__VA_ARGS__)
#define debugln(...) Serial.println(__VA_ARGS__)
#define debugf(...) Serial.printf(__VA_ARGS__)
#else
#define debug(...)
#define debugln(...)
#define debugf(...)
#endif

#define SD_MMC_CMD  38 //Please do not modify it.
#define SD_MMC_CLK  39 //Please do not modify it. 
#define SD_MMC_D0   40 //Please do not modify it.
#define ANIMATION_FOLDER "//animations"
#define DELIMITER ","
#define UNDEFINED -256
#define NONE "NONE"
#define EXTENSION ".csv"£


String HEADERS[] = {"index","blue","green","red"};


/**
 * Initialize the sdcard file system. 
 */
void sdmmcInit(void);


/**
 * Get the animation paths.
*/
String* getAnimationPaths(fs::FS &fs, const char* folderPath = ANIMATION_FOLDER);


/**
 * read frames from CSV files in a folder and return them as a list of frames
 */
std::vector<std::array<int, 4>> readFrames(const char* folderPath);

String free_mem(bool full = false);

#endif