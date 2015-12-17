from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from urllib.request import urlopen
import time

class ProxyProtocol(basic.LineReceiver):

    def lineReceived(self, line): # a more specific form of def dataReceived() from twisted.protocols.basic
        line = line.decode()
        if not line.startswith('http://') and not line.startswith('https://'):
            return
        start = time.time()
        print('fetching', line)
        data = urlopen(line).read()
        print('fetched', line)
        self.transport.write(data)
        self.transport.loseConnection()
        print('took', time.time() - start)

factory = protocol.Factory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)
reactor.run()

# (after having run 'python3 proxyserver.py' in a separate console tab)
# $ telnet localhost 8000
# [Trying 127.0.0.1...]
# [Connected to localhost.]
# [Escape character is '^]'.]
# http://www.nytimes.com/
# [<!DOCTYPE html>]
# [....]
# [....]
# [Connection closed by foreign host.]
# $


# time diff of threaded vs synch:
# (running multiclient, sending games.com and nytimes urls)
# fetching http://www.games.com/
# fetched http://www.games.com/
# took 1.2363109588623047
# fetching http://www.nytimes.com/
# fetched http://www.nytimes.com/
# took 0.14466404914855957
#
# (running threadedclient, sending games.com and nytimes urls)
# fetching http://www.games.com/
# fetched http://www.games.com/
# took 1.7874999046325684
# fetching http://www.nytimes.com/
# fetched http://www.nytimes.com/
# took 0.14489388465881348
