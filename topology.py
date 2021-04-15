from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.topo import Topo

setLogLevel( 'info' )

# ONOS
#c0 = RemoteController( 'c0', ip='127.0.0.1', port=6654)

#cmap = { 's1': c0, 's2':c0, 's3': c0}

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

class MyTopo( Topo ):
    "Simple topology example."

    def build(self):

        # Initialize topology
        #adding hosts
        #h1 = self.addHost('h1', mac='00:16:3E:34:7D:64')
        #h2 = self.addHost('h2', mac='00:16:3E:BF:74:13')
        #h3 = self.addHost('h3', mac='00:16:3E:4A:A4:4F')
        #h4 = self.addHost('h4', mac='00:16:3E:EA:80:5F')
        #h5 = self.addHost('h5', mac='00:16:3E:DD:97:A6')

		
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        #adding switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        #adding links
        self.addLink(s1, s3)
        self.addLink(s1, s4)
        self.addLink(s2, s3)
        self.addLink(s2, s4)
        self.addLink(h1, s1)
        self.addLink(h2,s2)


topos = { 'mytopo': ( lambda: MyTopo() ) }
#topo = MyTopo() 
#net = Mininet( topo=topo, switch=MultiSwitch, build=False )
#for c in [c0]:
#    net.addController(c)

##net.build()
#net.start()
#CLI( net )
#net.stop()
