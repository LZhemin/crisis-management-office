# Crisis Management Office

Project for CZ3003 Software System Analysis and Design, group SSP3.

## Getting Started Guide

### Getting Started for macOS and Unix-like

To run the server for this project, we will do the following:

1. Install `pip`
2. Install `virtualenv` and activate it
3. Install all python dependecies for this project
4. Run the server

First, we will install pip by following installation guide at 
https://pip.pypa.io/en/stable/installing/

```shell
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
```

Next, we will install `virtualenv` using `pip`, create a virtual environment, and activate the 
environment. 

```shell
$ sudo python -m pip install virtualenv
$ virtualenv cmoenv
$ source cmoenv/bin/activate
```

Next, we will install all requirements/dependencies for this project using `pip`.

```
$ pip install -r requirements.txt
```

Finally, we start the server using the followin command:

```shell
$ python manage.py runserver
```

At the end of our development, we call `deactivate` in command line to deactivate `virtualenv`.

We don't install these dependecies everytime when we want to develop for this project. A normal 
workflow would be:

```shell
$ source cmoenv/bin/activate
$ python manage.py runserver

# When you are done
$ deactivate
```

### Getting Started using Docker

This option would allow any platforms that are supported by Docker to build and run this project.
First, we need to install Docker from [www.docker.com](https://www.docker.com/). Then, run the
following command:

```
$ docker-compose up
```

## Linter and Formatter

We follow pep8 style guide for python.

To lint our codes:

```shell
$ pip install pylint
$ find CZ3003_SSP3_CMO myapp -iname "*.py" | xargs pylint
```

To format our codes:

```shell
$ pip install yapf
$ find CZ3003_SSP3_CMO myapp -iname "*.py" | xargs yapf -i
```
