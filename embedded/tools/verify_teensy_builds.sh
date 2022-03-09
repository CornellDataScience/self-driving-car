set -e # Exit on any error

# Run static analysis
cppcheck test src # lib/utils lib/Drivers lib/Devices lib/rwmutex

# Compile HOOTL/HITL/Flight Teensy environments
platformio run -e flight
