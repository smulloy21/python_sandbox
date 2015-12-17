import threading
from multiclient import make_connection

def t_connection(host, port, d):
    print('sending', d)
    print(make_connection(host, port, d.encode()))

if __name__ == '__main__':

    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    threads = []
    for d in data_to_send:
        t = threading.Thread(target = t_connection, args=(host, int(port), d))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('finished')

# (while running practice.py in seperate console tab)
# $ python3 threadedclient.py 127.0.0.1:8000 1 2 3 4 5
# sending 1
# sending 2
# sending 3
# sending 4
# sending 5
# There are 3 connections.
# Hi! Send me text to convert to uppercase:
# 3
#
# There are 5 connections.
# Hi! Send me text to convert to uppercase:
# 5
# There are 1 connections.
# Hi! Send me text to convert to uppercase:
# 1
#
# There are 4 connections.
# Hi! Send me text to convert to uppercase:
# 4
#
# There are 2 connections.
# Hi! Send me text to convert to uppercase:
# 2
#
#
# finished
# $
