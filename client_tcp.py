import socket
import pickle
import data_collection_client


def main_client():
        host = '10.42.43.1'
        port = 65432
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            print(f'[LOG] Connected to: {host}')
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                else:
                    data_to_receive = pickle.loads(data)
                    if data_to_receive == '0':
                        message = data_collection_client.all
                        data_to_send = pickle.dumps(message)
                        sock.send(data_to_send)
                    else:
                        ans = input('\nDo you want to continue(y/n): ')
                        if ans == 'y':
                            continue
                        else:
                            break
            print('[LOG] Connection closed')
            sock.close()
        except socket.error:
            print('[LOG] Problems with connection to server')
            print('[LOG] Connection closed')
            sock.close()


if __name__ == '__main__':
    main_client()