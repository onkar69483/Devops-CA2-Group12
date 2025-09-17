#!/bin/bash

# Fixed versionLT function to correctly compare version strings
versionLT() {
  # Returns 0 (true) if $1 < $2, 1 (false) otherwise
  [ "$1" = "$2" ] && return 1

  local IFS=.
  local i ver1=($1) ver2=($2)

  # fill empty fields in ver1 with zeros
  for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
    ver1[i]=0
  done

  for ((i=0; i<${#ver1[@]}; i++)); do
    if [[ -z ${ver2[i]} ]]; then
      # fill empty fields in ver2 with zeros
      ver2[i]=0
    fi
    if ((10#${ver1[i]} < 10#${ver2[i]})); then
      return 0
    elif ((10#${ver1[i]} > 10#${ver2[i]})); then
      return 1
    fi
  done
  return 1
}

# Example usage: Uncomment for manual testing
# versionLT "2.190" "2.200" && echo "2.190 < 2.200" || echo "Not less"
