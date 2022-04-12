# self-driving-car
This is a multi-year project undertaken by the Cornell Data Science team intended to demonstrate autopilot for a full-size car.

CDS Self-Driving Car aims to demonstrate tight integration of a camera based vision algorithm to navigate a car safely. We utilize a SLAM system to localize ourselves, and an additional lane recognition pipeline to see the road. This is all built upon a Python control loop and will leverage robotics to directly actuate the steering wheel to augment a normal car.

## Team
This ambitious project is being lead by Iris Li, Edward Gu, Tobi Alade, Elias Little, Eric Zhang, Adarsh Sriram, and Shihao Cao

## Current Status
Please take a look at our issue ticket board to see what we're currently working on!

## Organization and Workflow
We use a mixed HOOTL, HITL, and Flight-like testing/iteration strategy similar to SpaceX.

## Building and running docker
1. Download docker desktop: https://www.docker.com/products/docker-desktop
2. Build docker image
  - Run: "docker build --tag self-driving-car ."
3. Running the docker image
  - When QT works runDocker.sh script will setup enviorment/ permissions and run docker image
    - Run: "sh runDocker.sh"
  - For now comment out any display_frame refrences in main control loop
    - Then run: "sudo docker run self-driving-car python3 -m src config_file_name test_case_name"
    - For example: "sudo docker run self-driving-car python3 -m src hootl.yaml NoSIM"

*To edit the docker image, edit "dockerfile" 
*To edit the process of changing the enviorment and running the image, edit "runDocker.sh"

## Installation

See `INSTALL.md`.

## Run the MCL

Always remember to have the virtual environment `venv` activated with: 

```
. venv/bin/activate
```

# Linting
The linting will run automatically on every push and pull request but to check things locally uou can run:
- To run pylint, our main linter run:

```pylint src --fail-under=8```
- A pylint score under 8 will cause you to fail, fix output as shown on github or by running the command locally

* To change our linting requirements edit config.pylintrc

### Actually running the MCL

Our code is structured as a module: `src` we invoke it with for example:


```
python -m src hootl.yaml NoSIM
```

This means to use the `hootl.yaml` configuration file in `src/configs`, along with the
`NoSIM` testcase under `runner/`. You can go to those directories respectively to find more config files
and more test cases.
