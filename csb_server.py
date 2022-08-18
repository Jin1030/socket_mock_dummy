#!/usr/bin/python3

import argparse, socket, json
import sys
import urllib.request

BUFSIZE = 1024


def csb_server(host, port):
    
    # creat an socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a host and a port
    try:
        sock.bind((host, port))
    except socket.error as msg:
        print('# Bind failed. ')
        sys.exit()

    while True:
        sock.listen(1)
        conn, (mockhost, mockport) = sock.accept()
        print('We have accepted a connection from host:', mockhost)
        print('We have accepted a connection from port', mockport)
        
        # function to read the data ## todo: Needs to be rewritten
        def recv_data():
            try:
                data = conn.recv( BUFSIZE )
                print("\ndata: %s" % data.decode())
                return data
            except :
                sys.exit("no data RECEIVED!")
        data = recv_data()

        if "startinstallation" in data.decode():
            print("\n << startinstallation RECEIVED!")
            # send information to mockserver
            conn.send("fetch the information".encode())
            
            # receive the json data from mockserver 
            message = recv_data()
            if not message:
                print('# no data. ') # to do
                sys.exit() 
            reply = json.loads(message)
            # check the received data
            print('http_ip: ', reply['ip'])
            print('http_port: ', reply['port'])
            print("http://"+reply['ip']+":"+reply['port']+"/test/csb_conf.txt", "/home/user/csb_conf.txt")
            # download the files from local http server
            urllib.request.urlretrieve("http://"+reply['ip']+":"+reply['port']+"/test/csb_conf.txt", "/home/user/csb_conf.txt")
            break

        else:
            print("\n << startinstallation not RECEIVED!")
            break

    sock.close()




def main():

    parser = argparse.ArgumentParser(description='This is the csb server, which is used to simulate csb software.')
    parser.add_argument('host', help='interface that the server listens at;')
    parser.add_argument('-p', metavar='PORT', type=int, default=8000,
                        help='TCP port (default 8000)')
    args = parser.parse_args()
    print(args)

    # establish the csb server
    csb_server(args.host, args.p)


main()