# self-driving-car
This is a multi-year project undertaken by the Cornell Data Science team intended to demonstrate autopilot for a full-size car.

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
  - runDocker.sh script will setup enviorment/ permissions and run docker image
    - Run: "sh runDocker.sh"

*To edit the docker image, edit "dockerfile" 
*To edit the process of changing the enviorment and running the image, edit "runDocker.sh"

## Run the MCL

. venv/bin/activate
python -m src hootl.yaml NoSIM