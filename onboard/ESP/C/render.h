#pragma once
#ifndef RENDER_H
#define RENDER_H

#include <Adafruit_NeoPixel.h>
#include "io.h"

/**
 * Struct to hold Reandering information.
 */
struct Renderer {
    float BRIGHTNESS = 0.40;
    int SPEED = 1;
    int CHANNEL = 0;
    int PIN = 21;
    int LEDS = 100;
    bool RUNNING = true;
    Adafruit_NeoPixel SCREEN;

    /*
     * print rendering conf values.
     */
    void print() const {
        debugln("LEDS: " + String(LEDS));
        debugln("PIN: " + String(PIN));
        debugln("CHANNEL: " + String(CHANNEL));
        debugln("SPEED: " + String(SPEED));
        debugf("BRIGHTNESS: %f\n", BRIGHTNESS);
        debugln();
    }
};

/**
 * Read setting config file, save configuration to Renderer struct.
 */
void readSettingsConf(fs::FS &fs, const char *path, Renderer *renderer);

#endif