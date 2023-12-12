import sys
import logging
from scapy.all import *
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def process_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    data = []

    for packet in packets:
        try:
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            packet_size = len(packet)
            timestamp = packet.time
            data.append([src_ip, dest_ip, packet_size, timestamp])
        except (IndexError, AttributeError) as e:
            logging.error(f"Error processing packet: {e}")
            continue

    return data

def detect_ddos_attacks(data, eps=0.5, min_samples=5):
    df_src_ip = [row[0] for row in data]
    features = [[row[2], row[3]] for row in data]
    features = StandardScaler().fit_transform(features)

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(features)
    labels = db.labels_

    src_ips = [df_src_ip[i] for i, label in enumerate(labels) if label != -1]
    unique_src_ips = list(set(src_ips))

    rules = [f"-s {ip} -j DROP" for ip in unique_src_ips]
    return rules

if __name__ == '__main__':
    pcap_file = sys.argv[1]
    output_file = sys.argv[2]

    data = process_pcap(pcap_file)
    rules = detect_ddos_attacks(data)

    with open(output_file, 'w') as f:
        for rule in rules:
            f.write(f"{rule}\n")
