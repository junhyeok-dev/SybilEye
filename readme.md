# SybilEye

![version](https://img.shields.io/badge/version-0.1b-red) ![version](https://img.shields.io/badge/status-dev-red) ![version](https://img.shields.io/badge/build-failing-red) ![version](https://img.shields.io/badge/license-MIT-blue) ![version](https://img.shields.io/badge/dependencies-newest-green)

A sybil attack detection mechanism for mobile crowdsensing system. 

## Motivation

Mobile crowdsensing is a kind of data collection system that powered by crowd's mobile devices. By adopting mobile crowdsensing, you can collect sensing data without sensor installation. However, some users could provide fake sensing data to make your system malfunction. And attackers will compromise other user's ID and act like he/she is a group of users to improve attack efficiency. So, mobile crowdsensing system should have proper sybil attack detection mechanism to prevent the system from attackers. SybilEye is sybil attack detection mechanism for mobile crowdsensing system.

## Tech/framework used

* TShark
* Scapy

## Requirements

* TShark 2.6.8 or greater
* Scapy 2.4.3 or greater
* Python 3
* NIC with monitor mode enabled

## Features

SybilEye catch nodes suspended as sybil node(node that executing sybil attack).

## Installation

### Windows

1. Install Git, Python3, Wireshark(include TShark)

2. Set NIC monitor mode

3. Launch powershell(or cmd) and follow instruction

   ```sh
   pip install scapy
   
   git clone https://github.com/junhyeok-dev/SybilEye.git
   ```

### Linux(Ubuntu)

```sh
#Install requirements
sudo apt install git tshark python3 python3-pip
pip3 install scapy

#Set NIC monitor mode
sudo iwconfig INTERFACE down
sudo iwconfig INTERFACE mode monitor

#Download and Execute SybilEye
git clone https://github.com/junhyeok-dev/SybilEye.git
```

## How to use?

```sh
cd SybilEye
python3 SybilEye.py INTERFACE
```

A INTERFACE argument is interface name of monitor mode enabled NIC.

