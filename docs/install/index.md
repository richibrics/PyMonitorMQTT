# Install

Currently you need Python 3.7 to run PyMonitorMQTT; standalone executable files will be available soon (you won't need to install manually Python and all the requirements).


You can install Python 3.7 [here](https://www.python.org/downloads/).

### Install PIP

To install required packages you need [pip](https://www.makeuseof.com/tag/install-pip-for-python/)

#### Dependencies

To install dependencies all together, you only have to type in your terminal
```
python3 -m pip install -r requirements.txt
```

In addition, to get CPU temperature from Windows you need:
* wmi (module from pip): `python3 -m pip install wmi`
* Open Hardware Monitor (external software). [Download it](https://openhardwaremonitor.org/downloads/)
