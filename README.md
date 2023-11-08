# DataGen

Datagenerator for Masterthesis in the Project "Präzision-LDS"

Features:
    - Create timeseries with seeddata from csv's
    - Transform data through:
        - concatenating
        - smoothing, noising
        - scaling
        - ...
        - Injections: 
            - Anomalies
            - Pattern
    - Create additional feature that is related with seeddata features through Gaussian distribution


For using

> pip install requirements

The configurations can be set in the config.yaml. One example for a config file can be found in configExample.yaml.

Run datagenerator with:

> python -m dataGen

## Documentation

GutenTAG's documentation can be found [here](doc/index.md).

