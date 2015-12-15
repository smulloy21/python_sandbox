from twisted.internet import reactor, protocol, endpoints

class UpperProtocol(protocol.Protocol):

    def connectionMade(self):
        self.transport.write(b'Hi! Send me text to convert to uppercase:\n')
        # ^ inserts the data into a queue

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()
        # ^ comment out to keep connection running

factory = protocol.ServerFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)
reactor.run()


# (with server running in seperate console tab)
# $ telnet localhost 8000
# [Trying 127.0.0.1...]
# [Connected to localhost.]
# [Escape character is '^]'.]
# [Hi! Send me text to convert to uppercase:]
# type something in
# [TYPE SOMETHING IN]
# [Connection closed by foreign host.]
# $
