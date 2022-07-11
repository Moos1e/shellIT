# shellIT
## General Information
* Author: Jon Helmus
* Date 07/10/2022
* Description: A script that allows you to create reverse shell scripts that can be used for various CTF challenges.
* Video: https://youtu.be/15dL28OMVMU

## Installing
```
pip3 install netifaces
pip3 install arparse
```

## Usage
```
usage: shellIT.py [-h] [-p PORT] [-c CHOOSE [CHOOSE ...]] [iface]

Raining Shells!

positional arguments:
  iface                 <-- the network interface to use

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port number. Defaults to 4444 when not specified
  -c CHOOSE [CHOOSE ...], --choose CHOOSE [CHOOSE ...]
                        which command would you like to use?
