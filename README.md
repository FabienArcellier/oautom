[![Build Status](https://travis-ci.org/FabienArcellier/blueprint-webapp-flask.svg?branch=master)](https://travis-ci.org/FabienArcellier/blueprint-webapp-flask)

# OAutom

`oautom` is **educational** workflow engine implementation able to
run step by step treatment using directed acyclic graph (dag). It's not designed to use in production environment.

if you are looking for a mature workflow engine, you should take a look to
[`airflow`](https://airflow.apache.org/docs/stable/tutorial.html#setting-up-dependencies) from
which oautom reuse the declarative API.

## Getting started

```python
oautom = OAutom(mode='background')

# check execution status every minutes
oautom.refresh_schedule(minutes=1)

flow = Flow('flow 1', app=oautom)
step1 = LambdaExecution('lambda_name', flow=flow)
step2 = FargateExecution('task_definition', flow=flow)
step3 = LambdaExecution('lambda_arn', flow=flow)
step2.depends(step1)
step3.depends(step2)

oautom.start('flow 1')
status = oautom.status('flow 1')
```

more example in [oautom/examples](oautom/examples)

## Concepts

* a developer can implement an Execution that run a system and check if it's finish
* a developer can implement a Flow as a directed acyclic graph of steps
* only one instance of each flow may run in same time

### System requirements

The following requirements has to be setup on your host before running the command
from this repository.

* `python 3.6` at least
* [pipenv](https://pipenv.pypa.io/en/latest/)

### Install the python dependencies

```bash
make install_requirements_dev
make start
```

## The latest version

You can find the latest version to ...

```bash
git clone git@github.com:FabienArcellier/blueprint-webapp-flask.git
```

## Usage

You can run the application with the following command

```python
make start
```

## Contributing

### Install development environment

Use make to instanciate a python virtual environment in ./venv3 and install the
python dependencies.

```bash
make install_requirements_dev
```

### Freeze the library requirements

If you want to freeze all the packages, use
this procedure

```bash
make freeze_requirements
```

### Activate the python environment

When you setup the requirements, a `venv3` directory on python 3 is created.
To activate the venv, you have to execute /

```bash
make activate
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute pylint to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```

## Contributors

* Fabien Arcellier

## License

A short snippet describing the license (MIT, Apache, etc.)
