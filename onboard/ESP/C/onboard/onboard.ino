#include "render.h"
#include "io.h"

Renderer renderer;
std::vector<String> animations;
std::vector<std::vector<std::array<uint16_t, 4>>> frames;
Adafruit_NeoPixel neo;

/**
 * Memory printout. 
 */
void memory_printout() {
  debugln("Heap info:");
  debug("  Total heap size: ");
  debug(ESP.getHeapSize());
  debugln(" bytes");
  debug("  Free heap size: ");
  debug(ESP.getFreeHeap());
  debugln(" bytes");
  debug("  Maximum allocated heap size: ");
  debug(ESP.getMaxAllocHeap());
  debugln(" bytes");
  debugln();
}

void setup() {
  Serial.begin(115200);
  debugln();
  debugln("Setting up.");

  sdmmcInit();

  // Populate renderer struct with settings config.
  const char* settings = "settings.cfg";
  readSettingsConf(SD_MMC, settings, &renderer);

  //Initialize the screen.
  neo = Adafruit_NeoPixel(renderer.LEDS, renderer.PIN, NEO_GRB + NEO_KHZ800);

  // Initialize screen to render write to.
  neo.begin();
  neo.clear();
  neo.show();

  // Get the animation paths to look at.
  animations = getAnimationPaths(SD_MMC);
}   

void loop() {
  String animation_path = String(String(ANIMATION_FOLDER) + "/" + animations[renderer.CHANNEL]);
  frames.clear();
  frames = readFrames(SD_MMC, animation_path.c_str());

  memory_printout();

  uint16_t n, r, g, b;
  uint32_t pixelColor;
  const float brightness = renderer.BRIGHTNESS;

  while(renderer.RUNNING) {
    for (const auto& frame : frames) {
      for (const auto& p : frame) {
        
        n = p[0];
        r = static_cast<uint8_t>(p[3] * brightness);
        g = static_cast<uint8_t>(p[2] * brightness);
        b = static_cast<uint8_t>(p[1] * brightness);
        
        pixelColor = renderer.SCREEN.Color(r, g, b);
        renderer.SCREEN.setPixelColor(n, pixelColor);
      }
      renderer.SCREEN.show();
      delay(20);
    }
    debugln("PLAYED ALL FRAMES!");
    delay(1000);
  }  
}