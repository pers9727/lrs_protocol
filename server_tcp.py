import socket
import threading
from _thread import *
import pickle
import os
import work_with_files

module_file = '/home/roman/lrs_protocol/module_information/'
commands_file = '/home/roman/lrs_protocol/commands.txt'
ip_type_file = f'{os.getcwd()}/ip_type.txt'
print_lock = threading.Lock()
port = 65432


def threaded(conn, ip_addr):

    ip_family = '10.42.43.'
    conn.send(pickle.dumps('0'))
    module_data = f'{module_file}{ip_addr[len(ip_family):]}.txt'

    while True:
        # Get data from client
        data_to_receive = conn.recv(4096)
        # If data is None -> close connection
        if not data_to_receive:
            print('[LOG] Connection closed')
            print_lock.release()
            break
        # Data is getting
        else:

            # Write new data to new_data
            new_data = pickle.loads(data_to_receive)
            print(new_data)
            # Write ip_type to ip_type_data
            ip_type_data = f'{ip_addr} {new_data[0]}'


            # Write commands to file and check if command in file continue, else write
            for i in new_data[2]:
                if '\n' in i:
                    if i[:-1] in list('/home/pi/lrs_protocol/commands.txt'):
                        continue
                    else:
                        work_with_files.write(commands_file, str(i[:-1]) + '\n', 'a')
                else:
                    if i in list('/home/pi/lrs_protocol/commands.txt'):
                        continue
                    else:
                        work_with_files.write(commands_file, str(i) + '\n', 'a')
            # Write new_data to .txt file for new module
            for i in new_data:
                work_with_files.write(module_data, str(i) + '\n', 'a')

            # Create file with ip_type list of modules
            ''' if os.path.exists(ip_type_file) and os.stat(ip_type_file).st_size > 0:
                work_with_files.write(ip_type_file, ip_type_data, 'a')
            else:
                work_with_files.write(ip_type_file, ip_type_data, 'w')'''

    conn.close()


def main_client(port):
    host = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("[LOG] Socket created")

    try:
        sock.bind((host, port))
    except socket.error as msg:
        print("[LOG] ", msg)
    print("[LOG] Socket binded to port: ", port)

    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print_lock.acquire()
        print('[LOG] Connected with client: ', addr[0])
        start_new_thread(threaded, (conn, addr[0]))


if __name__ == '__main__':
    try:
        main_client(port)
    except KeyboardInterrupt:
        print('[LOG] Server stopped! Exit from protocol')
        exit()





