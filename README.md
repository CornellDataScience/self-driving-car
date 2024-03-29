# self-driving-car
This is a multi-year project undertaken by the Cornell Data Science team intended to demonstrate autopilot for a full-size car.

CDS Self-Driving Car aims to demonstrate tight integration of a camera based vision algorithm to navigate a car safely. We utilize a SLAM system to localize ourselves, and an additional lane recognition pipeline to see the road. This is all built upon a Python control loop and will leverage robotics to directly actuate the steering wheel to augment a normal car.

## Team
This ambitious project was undertaken by Evan Williams, Iris Li, Edward Gu, Tobi Alade, Elias Little, Eric Zhang, Adarsh Sriram, and Shihao Cao

# Demo Results:
FINAL PRESENTATION: https://docs.google.com/presentation/d/1MIJ480jFvm6mGaNohGM7KqMZyA3pAJ67wQSmTtvUBTY/edit?usp=sharing

# Moving Pieces:
Here's some extra details about each of the individual parts that we developed and how they work.

## Lane Detection
https://github.com/maunesh/advanced-lane-detection-for-self-driving-cars

## SLAM

## Main Control Loop Framework
The main control loop framework was based on a Read-Estimate-Control-Command-Actuate architecture inspired by work from the Pathfinder for Autonomous Navigation team.


## Embedded Systems

![Alt text](images/es-arch-hardware.jpg?raw=true "Hardware Stack")

Blah blah

<br>
<hr></hr>

![Alt text](images/embedded-systems-arch.jpg?raw=true "Embedded Systems Architecture")

# Hardware

![Alt text](images/hardware-stand.jpg?raw=true "Hardware Stand")

## Running it yourself
Please scroll to the bottom for continuation details.

# Running it Yourself

## Installation

See `INSTALL.md`.

## Run the MCL

Always remember to have the virtual environment `venv` activated with: 

```
. venv/bin/activate
```

### Actually running the MCL

Our code is structured as a module: `src` we invoke it with for example:


```
python -m src hootl.yaml NoSIM
```

This means to use the `hootl.yaml` configuration file in `src/configs`, along with the
`NoSIM` testcase under `runner/`. You can go to those directories respectively to find more config files
and more test cases.

## Hardware Setup

## HITL/Flight Configutaion
TODO insert everything required to do an in car demo.
