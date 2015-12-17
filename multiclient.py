import socket

def make_connection(host, port, data_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(data_to_send) # never use send, always use sendall
    s.sendall(b'\r\n')
    b = []
    while True:
        data = s.recv(1024)
        if data:
            b.append(data.decode()) # decode: wants a string to 'join' on ln 16
        else:
            break

    return ''.join(b)

if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    for d in data_to_send:
        print('sending', d)
        print(make_connection(host, int(port), d.encode())) # encode: has to be bytes


# (while running practice.py in seperate console tab)
# $ python3 multiclient.py 127.0.0.1:8000 some data to send
# sending some
# There are 1 connections.
# Hi! Send me text to convert to uppercase:
# SOME
#
# sending data
# There are 1 connections.
# Hi! Send me text to convert to uppercase:
# DATA
#
# sending to
# There are 1 connections.
# Hi! Send me text to convert to uppercase:
# TO
#
# sending send
# There are 1 connections.
# Hi! Send me text to convert to uppercase:
# SEND
#
# $
