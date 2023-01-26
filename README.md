# ***Object Oriented and Functional Programming with Python***
---
## **Habittracker Backend**

The clock strikes midnight and the rockets explode in the sky, which lights up in a variety of colors. The New Year is initiated and with it the New Year's resolutions.
But unfortunately, it is not always easy to successfully complete such resolutions in the following year.

Hence, to facilitate this and develop new positive habits, this project aims to create a habittracker backend as a command line application, with edit, manage, and analyze functionalities.

---

## **Installation instructions**

### **Python**

First, it is important to ensure that you have the latest version of Python installed. 

For this project Python 3.11.0 + is necessary. 

If you want to download Python or its latest version, you can find it [here](https://www.python.org/downloads/).

### **Setup**

After installing python its recommended to create a virtual environment to keep dependencies required for this project separate from other projects. 

(`python python3 -m venv “Name of the environment`)

Afterwards activate your environment by typing into your terminal:

(`python source “Name of the environment”/bin/activate`)

### **Requirements**

When you created and activated your virtual environment make sure pip is updated inside of your environment

(`python python -m pip install --upgrade pip`)

Afterwards install the following requirements:

•	Python 3.11.0 +

•	Rich 12.6.0 +
(`python pip install rich`)

•	Click 8.1.3 +

•	Typer 0.7.0 +
(`python pip install typer`)

•	Questionary 1.10.0 +
(`python pip install questionary`)

•	Pytest 7.2.0 +
(`python pip install pytest`)

To make things easiert you can just install the `requirements.txt`-file:

(`python pip install -r /path/to/requirements.txt`)

---

## **Usage**

Working with typer for building a command-line application and especially creating an command-line interface ( CLI ) there is one `start` command to launch the app:

(`python python -m habittracker start`)

By doing so you will receive an output like this, as your habittracker is empty:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2017.51.34.png)

Pressing `Y` or typing `Yes`, as the user is motivated to successfully complete his New Year's resolutions, the program will prompt the user to enter the name of his first habit:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2017.59.29.png)

After entering the name of the habit the program proceeds with a short description and choosing a periodicity.
After choosing for example a `Daily` periodicity the user is asked for a confirmation:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2018.23.33.png)

Confirming to this the user gets an overview of his first habit and the opportunity to head on to the starting page of this application which enables all the available functionalities:

![](Bildschirm%C2%ADfoto%202023-01-25%20um%2014.15.20.png)

---

### **Functionalities**

#### **Editing**

Here the user can `add` or `delete` a habit:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2018.12.38.png)

#### **Managing**

Here the user can `check-off` a habit:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2018.29.23.png)

#### **Analyzing**

Here the user can `analyze` the habits:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2018.32.03.png)

#### **Show Log**

The user gets a log overview of his habits:

![](Bildschirm%C2%ADfoto%202023-01-11%20um%2018.36.15.png)

---

### **Testing**

Additionally, you can run tests and confirm that the project is working correctly.
Therefore `pytest`, `datetime`, `CliRunner` from `typer.testing` and `freeze_time` from `freezegun` have to be imported.

For the test a `tests` folder was created with the `test_habittracker.py` file.
The Test class `TestHabit` contains only a `setup_method`. Hence, the test database will be created for testing and can be checked through the `DB Browser for SQLite`.

This browser can be downloaded [here](https://sqlitebrowser.org/dl/)

**Note** that the database has to be **deleted** in your `VS Code Explorer` before running a new test.

The tests of the predefined habits ( `Pushups`, `Drinking`, `Learning`, `Running`, and `Workout`) over 4 weeks will look like this :

The **habitbase**:

![](Bildschirm%C2%ADfoto%202023-01-24%20um%2018.02.54.png)

And the **habitlog**:

![](Bildschirm%C2%ADfoto%202023-01-24%20um%2018.03.08.png)

The test can be run by the command:

(`python -m pytest tests/test_habittracker.py`)

---

## **Contribution Guidelines**

I would welcome any kind of contributions to this project!! If there are any recommendations and you’re interested in helping, feel free to read the following guidelines and get started:

1.	**Fork** the repository and **clone** it to your local machine
2.	**Create a new branch** for your changes
3.	**Make your changes**, including tests, documentation, and any necessary code changes
4.	**Run tests** to ensure your changes do not break any existing functionality
5.	**Commit your changes** and push them to your fork
6.	**Submit** a pull request on the originals repository’s `master` branch

Be sure to include a detailed description of your changes, as well as any relevant information, such as issue numbers or screenshots.

And finally, thank you for contributing to this project!

---

## **Author**

Additionally feel free to contact me:

Name: Leon Fesser

E-Mail: leon.fesser@iubh.de
