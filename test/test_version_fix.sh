#!/bin/bash

source ../scripts/fix_version.sh

echo "Running version comparison tests..."

function test_version_pair {
  local v1=$1
  local v2=$2
  local expected=$3

  versionLT "$v1" "$v2"
  actual=$?
  if [ "$actual" -eq "$expected" ]; then
    echo "PASS: $v1 < $v2"
  else
    echo "FAIL: $v1 < $v2"
    exit 1
  fi
}

# Test cases: expected 0 = true, 1 = false
test_version_pair "2.190" "2.200" 0
test_version_pair "2.200" "2.190" 1
test_version_pair "2.200" "2.200" 1
test_version_pair "2.100.1" "2.100.2" 0
test_version_pair "2.100" "2.100.0" 1

echo "All tests passed!"
