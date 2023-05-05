import sys
import os
import pandas as pd
import numpy as np
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
        except IndexError:
            pass

    return pd.DataFrame(data, columns=['src_ip', 'dest_ip', 'packet_size', 'timestamp'])

def detect_ddos_attacks(df, eps=0.5, min_samples=5):
    features = df[['packet_size', 'timestamp']].values
    features = StandardScaler().fit_transform(features)

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(features)
    labels = db.labels_
    df['cluster'] = labels

    attack_clusters = df[df['cluster'] != -1].groupby('cluster').filter(lambda x: len(x) > min_samples)
    src_ips = attack_clusters['src_ip'].unique()

    rules = []
    for ip in src_ips:
        rules.append(f"-s {ip} -j DROP")

    return rules

if __name__ == '__main__':
    pcap_file = sys.argv[1]
    output_file = sys.argv[2]

    df = process_pcap(pcap_file)
    rules = detect_ddos_attacks(df)

    with open(output_file, 'w') as f:
        for rule in rules:
            f.write(f"{rule}\n")
