#!/usr/bin/env python3
"""Dart feedback loss and repeated target freshness contracts."""

import re
import unittest
from pathlib import Path


source = (Path(__file__).resolve().parents[1] / "Dart.hpp").read_text()
target_source = (Path(__file__).resolve().parents[1] / "DartTarget.hpp").read_text()


class DartP1Regression(unittest.TestCase):
    def test_feedback_loss_stops_control(self):
        for motor in (
            "motor_yaw_", "motor_pitch_", "motor_fric_front_right_",
            "motor_fric_front_left_", "motor_fric_back_left_",
            "motor_fric_back_right_", "push_motor_",
        ):
            with self.subTest(motor=motor):
                self.assertIsNone(
                    re.search(rf"(?m)^\s*{motor}->Update\(\);", source),
                    f"{motor} discards its online status",
                )

        for control in ("ControlYaw", "ControlFric", "ControlPushMotor"):
            body = source.split(f"void {control}(", 1)[1].split("\n  }", 1)[0]
            with self.subTest(control=control):
                self.assertIsNotNone(
                    re.search(r"(?:online|fault|status)", body, re.I),
                    f"{control} must gate stale feedback output",
                )

    def test_repeated_valid_target_stays_fresh(self):
        receive = source.split("if (dart_gimbal_suber.Available()) {", 1)[1].split("dart_gimbal_suber.StartWaiting();", 1)[0]
        self.assertIn("DartDetail::AcceptYaw(new_yaw", receive)
        helper = target_source.split("bool AcceptYaw(", 1)[1].split("}  // namespace DartDetail", 1)[0]
        self.assertLess(helper.find("last_received = now;"), helper.find("std::abs(new_yaw - target_yaw)"))


if __name__ == "__main__":
    unittest.main()
