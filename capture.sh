#!/bin/bash

# Configurable parameters
interface=eth0
dumpdir=/root/
max_packets=20000
attack_threshold=30000
capture_duration=300 # seconds
webhook_url="https://discord.com/api/webhooks/..."

# Logging function
log() {
    echo "$(date) $1" >> /var/log/packet_capture.log
    curl -H "Content-Type: application/json" -X POST -d "{\"content\":\"$1\"}" $webhook_url >/dev/null 2>&1
}

# Main loop
while true; do
    pkt_old=$(grep $interface: /proc/net/dev | cut -d :  -f2 | awk '{ print $2 }')
    sleep 1
    pkt_new=$(grep $interface: /proc/net/dev | cut -d :  -f2 | awk '{ print $2 }')

    if [[ ! "$pkt_old" =~ ^[0-9]+$ ]] || [[ ! "$pkt_new" =~ ^[0-9]+$ ]]; then
        log "Error fetching packet count."
        sleep 1
        continue
    fi

    pkt=$(( $pkt_new - $pkt_old ))
    echo -ne "\\r$pkt packets/s\\033[0K"

    if [ $pkt -gt $attack_threshold ]; then
        pcap_filename=$dumpdir/dump.$(date +"%Y%m%d-%H%M%S").pcap
        log "Under attack. Capturing packets..."
        sudo tcpdump -n -i $interface -s0 -c $max_packets -w $pcap_filename >/dev/null 2>&1 &
        capture_pid=$!
        sleep $capture_duration
        kill -HUP $capture_pid >/dev/null 2>&1
        log "Packets captured."
        curl -H "Content-Type: application/octet-stream" -X POST --data-binary "@$pcap_filename" $webhook_url >/dev/null 2>&1

        # Call the Python script to analyze the captured packets
        log "Analyzing packets and generating rules..."
        python3 ddos_analyzer.py $pcap_filename /tmp/rules.txt

        # Apply the generated rules
        log "Applying generated rules..."
        while read -r rule; do
            iptables -A INPUT $rule
        done < /tmp/rules.txt
    else
        sleep 1
    fi
done
