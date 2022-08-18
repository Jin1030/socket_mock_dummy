#!/usr/bin/python3

import argparse, socket, json
import sys

csb_host = "10.200.220.1"
csb_port = 8000
BUFSIZE = 1024


def Interact_with_csb(host, port, jsonfile):
    
    # creat an socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the csb server
    print("\n>> connecting to: %s:%s" % (host, port))
    sock.connect((host, port))

	# Send startinstallation to CSB server
    sock.send("startinstallation".encode())

    # Receive the message from CSB server
    data = sock.recv( BUFSIZE )
    if not data:
        print('# no data. ')
        sys.exit()
    elif "fetch the information" in data.decode():
        print("\n << fetch the information RECEIVED!")

        #send the json config file to CSB server
        json_data = json.dumps(jsonfile)
        sock.sendall(bytes(json_data,encoding="utf-8"))
    else:
        sys.exit()

'''
this function is used to read the json file
'''
def read_configfile(filepath):
    with open(filepath) as json_file:
        file_loaded = json.load(json_file)
        print(file_loaded)
        #data_size = (len(json.dumps(file_loaded).encode('utf-8')))
        #print('json_data_size: ', data_size)
        return file_loaded



def main():

    parser = argparse.ArgumentParser(description='This is the mockserver, which is used to interact with the csb server.')
    parser.add_argument('host', help='interface to be connected is;')
    parser.add_argument('-p', metavar='PORT', type=int, default=8000,
                        help='the port to be connected is')
    parser.add_argument('-f', help='the path to config json file', default = config.json)
    args = parser.parse_args()
    print(args)
    
    # read the json config file
    config_json = read_configfile(args.f)
    print('httpserver_ip: ', config_json['ip'])
    print('httpserver_port: ', config_json['port'])
    
    # interact with csb server
    Interact_with_csb(csb_host, csb_port, config_json)



main()