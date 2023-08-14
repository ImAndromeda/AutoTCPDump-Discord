# Packet Capture and DDoS Analyzer Script

This is a shell script that captures network traffic on a given network interface and stores it in a file. The script is designed to detect network attacks and analyze network traffic. It integrates with a Python script that processes the packet captures, detects potential DDoS attacks, and generates iptables rules to block the malicious traffic. For the script to run successfully, `tcpdump` should be installed on your Linux machine along with the necessary Python packages.

# Download Here: [GitHub Repository](https://github.com/ImAndromeda/AutoTCPDump-Discord)

## For any issues, please create an issue on this repo

# Requirements

* Python 3.x
* tcpdump
* scikit-learn
* scapy

# Installation

1. Install the required Python packages:
```pip install scikit-learn scapy```

2. Install tcpdump:

## On Debian/Ubuntu: 
`sudo apt-get install tcpdump`

## On CentOS/RHEL: 
`sudo yum install tcpdump`

# Usage

1. Copy the script to a Linux machine.
2. Edit the configurable parameters at the beginning of the script to match your needs.
3. Run the script with `sudo` or as root.

`sudo ./capture.sh`

# Configuration

The following configurable parameters can be edited at the beginning of the script:

* `interface`: The network interface to capture traffic on.
* `dumpdir`: The directory to store the captured packet files.
* `max_packets`: The maximum number of packets to capture before stopping.
* `attack_threshold`: The threshold for detecting a network attack. If the number of packets per second exceeds this threshold, the script will capture packets.
* `capture_duration`: The duration of the packet capture in seconds.
* `webhook_url`: The URL of the Discord webhook to send messages and packet captures to. This should ideally be moved to a configuration file for security purposes.

# Customization

The script can be customized in various ways:

* Change the `interface` parameter to capture traffic on a different network interface.
* Modify the `dumpdir` parameter to store captured packet files in a different directory.
* Adjust the `max_packets` and `capture_duration` parameters to capture more or less traffic.
* Modify the `attack_threshold` parameter to detect attacks with a different packet rate threshold.
* Customize the `log()` function to send notifications to different channels or services.
* Extend the script by adding more functionalities, like deeper packet analysis or integration with other security tools.
