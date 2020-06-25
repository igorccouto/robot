# Robot

On this project, you will find a robot to perform several actions in the browser using [Selenium WebDriver](https://www.selenium.dev/).

## Project Organization
------------

The use of *pipenv* instead of *pip* is encouraged on this project.

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Folder to keep files (.CSV) consumed by the robot.
    ├── driver             <- Webdriver executable will be placed here.
    ├── notebooks          <- Jupyter notebooks.
    ├── settings.py        <- Settings module.
    ├── setup.py           <- makes project pipenv installable (pipenv install -e .) so robot can be imported.
    ├── robot              <- Source code for use in this project.
    ├── tests              <- Test code of the project.
    ├── Pipfile            <- Information about dependencies of the project.
    └── Pipfile.lock       <- To create deterministic builds.

## Before usage

1. Download and install [Python 3.8](https://www.python.org/downloads/release/python-383) for your system.
2. Install *pipenv*:
    - Windows:
        ```
        $ pip install pipenv
        ```
    - On Linux, you can use apt too:
        ```
        $ sudo apt install pipenv
        ```

3. Install the dependencies of the project.
    - In production:
        ```
        $ pipenv install
        ```
    - In development:
        ```
        $ pipenv install --dev
        ```
4. Your robot is ready!