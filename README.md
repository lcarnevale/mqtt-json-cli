# MQTT JSON Interface Command Line
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This project contains an interface for exchanging JSON messages through MQTT protocol. It is usable by means of command line.

## How to Install It
Create the virtual environment.
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

## How to Run It
Subscribe to a MQTT Broker as follow. The example below uses the [public broker](https://mqtt.eclipse.org/) hosted by Eclipse.
```bash
python subscriber.py --host mqtt.eclipse.org -t /mytopic/test
```

Publish then JSON data as follow. 
```bash
python publisher.py --host mqtt.eclipse.org --topic /mytopic/test --data "{\"key\": \"value\"}"
```