"""
    This script cleans up output from the netstat'ed connection log from a honeypot.

    The netstat output is preprocessed as follows:

    Screen running the following:
    while true; do netstat -p --numeric-hosts | grep nyancat | tee -a conn.log; echo "" >> conn.log; sleep 1; done

    conn.log processed to uniq-conns.log with the following
    cat conn.log | awk '{print $5}' | awk /./ | sort | uniq | awk '{split($1, a, ":"); print a[1]}' | uniq > uniq-conns.log

"""
import os
import sys
import socket

USAGE="Usage:\npython clean.py uniq-conns.log iplist.file"

"""
    Idea From https://stackoverflow.com/questions/11264005/using-a-regex-to-match-ip-addresses-in-python
    Determine if an address is a valid ip address using socket library
"""
def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

"""
    Process a string with potnetial ip addresses encoded with other data and dots as dashes
"""
def process_ip(address):
    ipTokens = address.replace("-", ".").split(".")
    newTokens = []
    for token in ipTokens:
        try:
            # Check if tokens are integers
            newTokens.append(str(int(token)))
        except:
            continue
    if len(newTokens) == 4:
        # If 4 valid int tokens then we assume its an IP address
        return '.'.join(newTokens)
    else:
        # Otherwise let valid_ip figure it out
        return address

"""
    Process a raw log file to pure IP Address file
"""
def process_file(raw_file, output_file):
    print("Reading from {} to {}".format(raw_file, output_file))
    with open(raw_file, 'r') as fin:
        with open(output_file, 'w') as fout:
            while True:
                line = fin.readline()
                if not line:
                    break
                line = line.strip()
                processedIP = process_ip(line)
                if valid_ip(processedIP):
                    fout.write(processedIP + "\n")
                else:
                    print(processedIP)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print(USAGE)
        exit(1)
    else:
        IP_LIST = os.path.join(os.getcwd(), sys.argv[1])
        OUTPUT_FILE = os.path.join(os.getcwd(), sys.argv[2])
    process_file(IP_LIST, OUTPUT_FILE)