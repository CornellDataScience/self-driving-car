# lodestar
Lodestar is a small scale electric demonstrator for the belly-flop and tail-sitting control algorithms necessary for SpaceX's Starship.

This project is being undertaken by Shihao Cao and Govind Chari

## Setup

This project is setup within VSCode and leverages the PlatformIO extension heavily. This project also borrows a lot of framework code from the Cornell Space Systems Design Studio project: Pathfinder for Autonomous Navigation (PAN).

Link to PAN repo:
https://github.com/pathfinder-for-autonomous-navigation

### Installations

You will need the latest Teensyduino, and a compatible version of Arduino.

You will need VSCode and the Platformio extension.

## Uploading Code

This command will upload the current flight software stack.
This project assumes you have a Teensy 3.6 plugged in.
```
pio run -e flight -t upload
```

You can replace the `flight` environment with your own enviorment as configured in `platformio.ini`.

The below environment is linked to the `your_target.cpp` file.
```
pio run -e your_target -t upload
```

You can check your code compiles without uploading through:
```
pio run -e your_target
```

For more information, google `pio run`, and change the `platformio.ini` accordingly.

## Groundstation

To start the Flask server that reads from either hardline serial or the 915 MHz Telemetry Radio:
```
cd web/flask
. start
```

To start the ground station website:
```
cd web/gs
npm start
```

## FAQ / Fixes
Error:
> error: there are no arguments to 'isnan' that depend on a template parameter, so a declaration of 'isnan' must be available

If you run into a isnan() definition error in utility/vector.h in the Adafruit BNO_055 library within the .pio folder, change `#include <math.h>` to `#include <cmath>` and `isnan()` to `std::isnan()`within the utility/vector.h file.

## BNO055 Calibration

Run
```
pio run -e imu_calibration -t upload
```

Place the imu on with every face of the chip pointing up to the sky. Basically try to have the imu sit on each face for 3 to 5 seconds.
Repeat this until the IMU is fully calibrated. You are waiting until the 3rd integer reaches 3 (the accelerometer calibration state).
All the other integers should reach 3 before the accelerometer does.

Once all sensors have been fully calibrated, the script will print out 50 lines of calibration state.
They should all be the same integers. If they are changing from line to line, the calibration failed.

Grab one of those lines, and save it. That line is the calibration offsets.

### Flight vs Ground Testing

You may want to use preloaded offsets so that for flight software development, you don't need to calibrate on every run.
However, I would recommend for a real flight to calibrate at the range.

## Sensor Checkouts

To check the functionality of the GPS:
```
pio run -e gps_serial
```

TODO: Other sensors

## Github Basics

To checkout the most recent changes, make sure you're on master, then pull the changes.
Angle brackets indicate template.

```
git checkout master
git pull
```

If there are conflicts and you're sure your work is not relevant or saved externally to this directory:
```
git reset --hard
```

To reset to origin
```
git reset --hard origin/master
```

To create a new branch from master:
```
git checkout -b "dev/<feature>"
```

To index changes, commit changes, and push them to the branch you're working on:
```
git add .
git commit -m "Added XYZ to ABC"
git push
```

To merge master's code into your branch, first commit your current
changes on `dev/<feature>`. Then:

```
git checkout master
git pull
git checkout dev/<feature>
git merge master
```

To update submodules:
```
git submodule update --init --recursive
```

If platformio is having issues linking libraries try:
This removes cached compiled files
```
pio run -t clean
```