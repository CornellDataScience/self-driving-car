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
The linting will run automatically on every push to master but to check things locally uou can run:
- "sh code_formatter.sh" to format code
- "sh import_formatter.sh" to format import statements
- "sh pylint.sh" to run pylint, our main linter
* All of these files are under "scripts"
* To change our linting requirements edit config.pylintrc