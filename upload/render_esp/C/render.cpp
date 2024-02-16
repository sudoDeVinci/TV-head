#include "render.h"

void animate(std::vector<std::array<int, 4>>* frames, Renderer* renderer) {
  for (auto& frame : *frames) {
    for (auto& p : frame) {
      int r = static_cast<int>(p[1] * renderer->BRIGHTNESS);
      int g = static_cast<int>(p[2] * renderer->BRIGHTNESS);
      int b = static_cast<int>(p[3] * renderer->BRIGHTNESS);
      renderer->SCREEN->setPixelColor(static_cast<uint16_t>(p[0]), r, g, b);
    }
    renderer->SCREEN->show();
    delay(renderer->SPEED * 20);
  }
}