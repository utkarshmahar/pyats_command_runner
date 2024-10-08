### pyats_command_runner 

This utility is used to fetch outputs of commands from various network devices. 


## Getting Started

Follow below instructions to setup the environment for running the script.

## Prerequisites

Python <= 3.10.X


## Installation

Setup virtual environment (optional)
```
python3 -m venv virtual_env
source virtual_env/bin/activate

```
Install python dependencies

```
pip3 install -r requirements.txt 

```


## Usage


```
python3 run.py -h
usage: run.py [-h] -wb WORKBOOK -ws WORKSHEET [-w WEBEX] [-ssh SSH_OPTIONS]

options:
  -h, --help            show this help message and exit
  -wb WORKBOOK, --workbook WORKBOOK
                        Workbook Name
  -ws WORKSHEET, --worksheet WORKSHEET
                        Worksheet Name
  -w WEBEX, --webex WEBEX
                        Webex
  -ssh SSH_OPTIONS, --ssh_options SSH_OPTIONS
                        SSH Options for old ciphers
```

The script takes 2 mandatory parameters

1. Workbook
     - This is the name of the excel sheet 
     - The first worksheet is called 'testbed'. It contains hostname, ip addresses and os of various devices
     
      
2. Worksheet
     - This is the name of a worksheet in the workbook
     - A workbook can have any number of worksheet
     - Each worksheet can group various devices and commands in any combinations


 ### Example 1


```
python3 run.py -wb cml_labs.xlsx -ws nexus_switches

```

### Example 2

```
python3 run.py -wb cml_labs.xlsx -ws nexus_switches -ssh " -o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 -o HostkeyAlgorithms=+ssh-rsa"

```

### Example 3


```
python3 run.py -wb cml_labs.xlsx -ws nexus_switches -w webex.yaml -ssh " -o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 -o HostkeyAlgorithms=+ssh-rsa"
```



## Demo


### Initializing script 
![Alt text](https://imgur.com/sRxDHTL.gif) 


### Data Gathering 


![Alt text](https://imgur.com/8UYCetj.gif) 




![Alt text](https://imgur.com/aPOBh5x.gif) 



### Final Reports




![Alt text](https://imgur.com/aPOBh5x.gif) 

![Alt text](https://imgur.com/KFXYk40.gif) 

