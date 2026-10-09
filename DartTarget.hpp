#pragma once

#include <cmath>

namespace DartDetail {
template <typename Timestamp>
bool AcceptYaw(float new_yaw, float& target_yaw, Timestamp& last_received,
               Timestamp now) {
  if (!std::isfinite(new_yaw) || new_yaw == 0.0f) {
    return false;
  }
  last_received = now;
  if (std::abs(new_yaw - target_yaw) <= 1e-6f) {
    return false;
  }
  target_yaw = new_yaw;
  return true;
}
}  // namespace DartDetail
