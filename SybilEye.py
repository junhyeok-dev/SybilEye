import subprocess
import sys
from scapy.all import *
import time

is_ap_encrypted = True
reject_ips = ["ff:ff:ff:ff:ff:ff", ""]
connected = []
disconnected = []
pairs = []
interface = sys.argv[1]

def emitARP(arr_result):
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.0.0/24"),timeout=2)
        ans.summary(lambda s: arr_result.append(s[1].sprintf("%Ether.src%")))

#Check whether AP in encrypted
arp_response = []
emitARP(arp_response)

connected = arp_response.copy()

if len(arp_response) < 2:
        is_ap_encrypted = True
        print("Your Wi-Fi network has encrypted!")
else:
        print("Your Wi-Fi network is opened")

#Start TShark WLAN packet capture
capture = subprocess.Popen([\
'tshark', '-l', '-i', interface, '-a', 'duration:60', '-T', 'fields',\
'-e', 'wlan.sa', '-e', 'wlan.da', '-e', 'wlan.fc.type_subtype'\
], stdout=subprocess.PIPE)

#Generate rejected IPs(include AP) list
linecount = 0

while linecount < 300:
        line = capture.stdout.readline()
        if line != b'':
                line = line.decode('utf-8')
                sa, da, subtype = line.split('\t')
                subtype = int(subtype)

                if subtype in [5, 8] and sa not in reject_ips:
                        reject_ips.append(sa)
                linecount += 1

print("Rejected IPs:", reject_ips)

#Start sybil node detection
if is_ap_encrypted:
	while True:
                line = capture.stdout.readline()
                if line != b'':
                        line = line.decode('utf-8')
                        
                        sa, da, subtype = line.split('\t')
                        subtype = int(subtype)

                        if subtype == 1 and da not in reject_ips:
                                print(da, " connected")
                                connected.append(da)
                                if len(disconnected) == 0:
                                        pairs.append(['', da])
                                else:
                                        for conn in disconnected:
                                                pairs.append([conn, da])   

                        tmp = ''
                        if subtype == 12 and sa not in reject_ips and sa != tmp:
                                tmp = sa
                                print(sa, " disconnected")
                                if sa not in disconnected:
                                        disconnected.append(sa)
                else:
                        conn, disconn = [], []
                        for pair in pairs:
                                conn.append(pair[1])
                                disconn.append(pair[0])

                        print(conn, disconn)

                        len_pairs = len(pairs)
                        i = 0
                        while i < len_pairs:
                                if conn[i] not in disconn[i + 1:]:
                                        print('conn ', conn[i], ' removed')
                                        del conn[i]
                                        del disconn[i]
                                        del pairs[i]
                                        len_pairs -= 1
                                else:
                                        i += 1

                        print(pairs)
                        
                        break
                
else:
        while True:
                line = capture.stdout.readline()
                if line != b'':
                        line = line.decode('utf-8')
                        
                        sa, da, subtype = line.split('\t')
                        subtype = int(subtype)

                        tmp = ""
                        
                        if subtype == 5 and da not in connected and da != tmp:
                                tmp = da
                                print(da, " connected")
                                new_connected = [da]
                                emitARP(new_connected)

                                print(new_connected)

                                for conn in connected:
                                        if conn not in new_connected:
                                                disconnected.append(conn)
                                                print(conn, ' disconnected')

                                connected = new_connected.copy()

                else:
                        break




