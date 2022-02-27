# SWA course - HW1

## Core libraries
- [fastapi](https://fastapi.tiangolo.com/)
- [requests](https://docs.python-requests.org/en/latest/)

## Prerequisities
- [python](https://www.python.org/) 3.8+
- [anaconda](https://docs.anaconda.com/anaconda/install/index.html)

## Setup
```
conda env create -f environment.yml --name HW1
conda activate HW1
```

## Usage
```
usage: main.py [-h] [--config CONFIG] [--facade] [--logging] [--messages]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        config with ports
  --facade              start facade service
  --logging             start logging service
  --messages            start messages service
```