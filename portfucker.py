import threading
from queue import Queue
import time
import socket
import sys
import signal
import os
import argparse
from termcolor import colored
parser = argparse.ArgumentParser(description="Port Fucker | Coded By https://github.com/rootkral4")

parser.add_argument("-i", "--ip", required=True, help="Ip address of host", type=str)
parser.add_argument("-r", "--range", required=False, default="0,1001", help="Scan range default 0,1000", type=str)
parser.add_argument("-t", "--threads", required=False, default=50, help="Threads default 50", type=int)

args = parser.parse_args()
attackip = getattr(args,'ip')
scanrange = getattr(args,'range')
threads = getattr(args,'threads')

scanrange = scanrange.split(",")

print_lock = threading.Lock()

socket.timeout(5)

global portactive
global portlist
portlist = []
portactive = True

print(colored("     👑 For Real Kings 👑    ", "green"))
print(colored("-" * 40, "magenta"))
print(colored("Url              :" + str(attackip), "green"))
print(colored("Port Scan Range  :" + str(scanrange[0]) + "-->" + str(scanrange[1]), "green"))
print(colored("Threads          :" + str(threads), "green"))
print(colored("-" * 40, "magenta"))
print(colored("rootkral4 | https://github.com/rootkral4","green"))


def portscan(attackip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((attackip,port))
        with print_lock:
            portlist.append(port)
        con.close()
    except:
        pass
    print("[*] Now Scanning {} [*]".format(port), end="\r")
    if port == int(scanrange[1]):
        portactive = False
        ports = ""
        for port in portlist:
            ports += str(port) + ","        
        print(colored("[!] Port Scan Done, Ports ;\n{}\n".format(ports[:-1]),"green"))
        os.system("nmap {} -p {} {} -sV".format(attackip, ports[:-1], "-Pn"))
        os.kill(os.getpid(), signal.SIGTERM)



def threader():
    while True:
        worker = q.get()
        portscan(attackip, worker)
        q.task_done()
        if portactive == False:
            break


q = Queue()

for x in range(threads):
     t = threading.Thread(target=threader, daemon=True).start()

for worker in range(int(scanrange[0]),int(scanrange[1]) + 1):
    q.put(worker)

q.join()