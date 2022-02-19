# self-driving-car
This is a multi-year project undertaken by the Cornell Data Science team intended to demonstrate autopilot for a full-size car.

## Team
This ambitious project is being lead by Iris Li, Edward Gu, Tobi Alade, Elias Little, Eric Zhang, Adarsh Sriram, and Shihao Cao

## Current Status
Please take a look at our issue ticket board to see what we're currently working on!

## Organization and Workflow
We use a mixed HOOTL, HITL, and Flight-like testing/iteration strategy similar to SpaceX.


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