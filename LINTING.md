# Linting
The linting will run automatically on every push and pull request but to check things locally uou can run:
- To run pylint, our main linter run:

```pylint src --fail-under=8```
- A pylint score under 8 will cause you to fail, fix output as shown on github or by running the command locally

* To change our linting requirements edit config.pylintrc