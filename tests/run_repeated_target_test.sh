#!/usr/bin/env bash
set -euo pipefail
test_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
module_root="$(cd "$test_dir/../.." && pwd)"
libxr="$module_root/../Middlewares/Third_Party/LibXR"
includes=(-I"$module_root/CMD" -I"$module_root/RMMotor" -I"$module_root/Motor" -I"$module_root/Referee")
while IFS= read -r -d '' path; do includes+=(-isystem "$path"); done < <(find "$libxr/src" -type d -print0)
"${CXX:-c++}" -std=c++20 -Wall -Wextra -Werror \
  -DLIBXR_DEFAULT_SCALAR=float -DXR_LOG_MESSAGE_MAX_LEN=128 \
  -isystem "$libxr/system/linux" -isystem "$libxr/lib/Eigen" \
  "${includes[@]}" "$test_dir/repeated_target_test.cpp" \
  -o /tmp/dart_repeated_target_test
/tmp/dart_repeated_target_test
