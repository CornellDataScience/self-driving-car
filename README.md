# self-driving-car
This is a multi-year project undertaken by the Cornell Data Science team intended to demonstrate autopilot for a full-size car.

## Team
This ambitious project is being lead by Iris Li, Edward Gu, Tobi Alade, Elias Little, Eric Zhang, Adarsh Sriram, and Shihao Cao

## Current Status
Please take a look at our issue ticket board to see what we're currently working on!

## Organization and Workflow
We use a mixed HOOTL, HITL, and Flight-like testing/iteration strategy similar to SpaceX.


## Run the MCL

. venv/bin/activate
python -m src hootl.yaml NoSIM

# Linting
The linting will run automatically on every push and pull request but to check things locally uou can run:
- To run pylint, our main linter run:
  - ```pylint src --fail-under=8```
- To automatically format our code run:
  - ```yapf --in-place src/*.py```
- To automatically format import statements run:
  - ```autoflake --in-place --remove-unused-variables --remove-all-unused-imports *.py```
  - ```isort .```


* To change our linting requirements edit config.pylintrc