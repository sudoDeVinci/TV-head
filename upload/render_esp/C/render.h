#pragma once
#ifndef RENDER_H
#define RENDER_H
#include <ESP32.h>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

struct Renderer {
    float BRIGHTNESS = 0.4;
    int SPEED = 1;
    int CHANNEL = 0;
    int Pin = 21;
    int LEDS = 96;
    bool RUNNING = false;
    Adafruit_NeoPixel* SCREEN;
} renderer;

void animate(std::vector<std::array<int, 4>>* frames, Renderer* renderer);

#endif