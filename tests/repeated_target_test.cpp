#include <cassert>
#include <limits>

#include "../DartTarget.hpp"

int main() {
  float target = 0.0f;
  unsigned last_received = 0;
  assert(DartDetail::AcceptYaw(1.25f, target, last_received, 10U));
  assert(target == 1.25f && last_received == 10U);

  assert(!DartDetail::AcceptYaw(1.25f, target, last_received, 90U));
  assert(target == 1.25f && last_received == 90U);

  assert(!DartDetail::AcceptYaw(0.0f, target, last_received, 100U));
  assert(!DartDetail::AcceptYaw(std::numeric_limits<float>::quiet_NaN(), target,
                                last_received, 110U));
  assert(last_received == 90U);
}
