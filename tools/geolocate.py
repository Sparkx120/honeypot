##
# This script calls the abstractapi.com api for ip geolocation based on a file with ip addresses on each line
# 
# To use this script you must provide the abstractapi.com geolocation api key through environment with
# ABSTRACT_API=<your_api_key>
#
# Use clean.py to clean logs into the write format
##
import requests
import os
import sys
import time

USAGE="Usage:\npython geolocate.py iplist.file output.file"
ABSTRACT_API = os.environ['ABSTRACT_API']
API_ENDPOINT = "https://ipgeolocation.abstractapi.com/v1/?api_key={}&ip_address={}"
API_TIME_RATE_LIMIT = 1
API_RETRY_LIMIT = 3

"""
    Geolocate IP Address list from ipaddress file
"""
def process_file(raw_file, output_file):
    print("Reading from {} to {}".format(raw_file, output_file))
    with open(raw_file, 'r') as fin:
        with open(output_file, 'w') as fout:
            while True:
                line = fin.readline()
                if not line:
                    break
                ip_address = line.strip()
                print("Processing IP Address: {}".format(ip_address))
                tries = 0
                status = 0
                content = ""
                while tries < API_RETRY_LIMIT and status != 200:
                    tries = tries + 1
                    response = requests.get(API_ENDPOINT.format(ABSTRACT_API, ip_address))
                    status = response.status_code
                    content = response.content.decode('utf-8')
                    time.sleep(API_TIME_RATE_LIMIT)
                if tries == API_RETRY_LIMIT:
                    print("API Error {}!".format(status))
                    exit(1)
                fout.write(content + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print(USAGE)
        exit(1)
    else:
        IP_LIST = os.path.join(os.getcwd(), sys.argv[1])
        OUTPUT_FILE = os.path.join(os.getcwd(), sys.argv[2])
    process_file(IP_LIST, OUTPUT_FILE)
