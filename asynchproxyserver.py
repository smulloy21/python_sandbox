from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.web.client import getPage
import time

class ProxyProtocol(basic.LineReceiver):

    def lineReceived(self, line):
        if line.decode().startswith('http://'): # problem with SSL?
            start = time.time()
            print('fetching', line)
            def gotData(data):
                print('fetched', line)
                self.transport.write(data)
                self.transport.loseConnection()
                print('took', time.time() - start)
            deferredData = getPage(line)
            deferredData.addCallback(gotData)


factory = protocol.Factory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()


# time diff of threaded vs synch:
# (running multiclient, sending games.com and nytimes urls)
# fetching b'http://www.games.com/'
# fetched b'http://www.games.com/'
# took 1.4044749736785889
# fetching b'http://www.nytimes.com/'
# fetched b'http://www.nytimes.com/'
# took took 0.1579289436340332
#
# (running threadedclient, sending games.com and nytimes urls)
# fetching b'http://www.games.com/'
# fetching b'http://www.nytimes.com/'
# fetched b'http://www.nytimes.com/'
# took 0.17345905303955078
# fetched b'http://www.games.com/'
# took 1.3143668174743652
