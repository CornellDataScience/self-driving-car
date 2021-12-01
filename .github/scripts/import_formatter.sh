pip install isort
pip install autoflake

autoflake --in-place --remove-unused-variables --remove-all-unused-imports *.py # Remove unused variables and import statements

isort . # Sort import statements correctly
