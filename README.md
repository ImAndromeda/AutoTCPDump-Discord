# Packet Capture Script

This is a shell script that captures network traffic on a given network interface and stores it in a file. The script is useful for detecting network attacks and analyzing network traffic. You will need to have `tcpdump` installed on your Linux machine.

## Usage

1. Copy the script to a Linux machine.
2. Edit the configurable parameters at the beginning of the script to match your needs.
3. Run the script with `sudo` or as root.

## Configuration

The following configurable parameters can be edited at the beginning of the script:

* `interface`: The network interface to capture traffic on.
* `dumpdir`: The directory to store the captured packet files.
* `max_packets`: The maximum number of packets to capture before stopping.
* `attack_threshold`: The threshold for detecting a network attack. If the number of packets per second exceeds this threshold, the script will capture packets.
* `capture_duration`: The duration of the packet capture in seconds.
* `webhook_url`: The URL of the Discord webhook to send messages and packet captures to.

## Customization

The script can be customized in the following ways:

* Change the `interface` parameter to capture traffic on a different network interface.
* Change the `dumpdir` parameter to store captured packet files in a different directory.
* Adjust the `max_packets` and `capture_duration` parameters to capture more or less traffic.
* Change the `attack_threshold` parameter to detect attacks with a different packet rate threshold.
* Modify the `log()` function to send notifications to different channels or services.
* Add additional functionality to the script, such as analyzing captured packets or running other security tools.
