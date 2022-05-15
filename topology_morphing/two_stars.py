#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from ipaddress import ip_address
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

# Node implementing a linux router, source: https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py
class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

    def startRouting(self):
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
    
    def stopRouting(self):
        self.cmd( 'sysctl net.ipv4.ip_forward=0')


def defineNet():
    net = Mininet( controller = RemoteController, waitConnected=True  )

    info( '*** Adding controller\n' )
    c0 = net.addController( 'c0' )

    info( '*** Adding switches\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip="192.168.1.1/24")
    h2 = net.addHost( 'h2', ip="192.168.1.2/24")
    h3 = net.addHost( 'h3', ip="192.168.1.3/24")
    h4 = net.addHost( 'h4', ip="192.168.1.4/24")
    h5 = net.addHost( 'h5', ip="192.168.2.1/24")
    h6 = net.addHost( 'h6', ip="192.168.2.2/24")
    h7 = net.addHost( 'h7', ip="192.168.2.3/24")
    h8 = net.addHost( 'h8', ip="192.168.2.4/24")
    h9 = net.addHost( 'h9', ip="192.168.1.254/24", cls=LinuxRouter)

    net.addLink( h1, s1) 
    net.addLink( h2, s1)
    net.addLink( h3, s1)
    net.addLink( h4, s1)

    net.addLink( h5, s2)
    net.addLink( h6, s2)
    net.addLink( h7, s2)  
    net.addLink( h8, s2)

    net.addLink( s1, h9, intfName1='s1-eth5', intfName2='h9-eth1') 
    net.addLink( s2, h9, intfName1='s2-eth5', intfName2='h9-eth2', params2={'ip' : "192.168.2.254/24"} )
    
    net.configLinkStatus("s1", "h9", "down")
    net.configLinkStatus("s2", "h9", "down")
    
    info( '*** Starting network\n')
    net.start()

    
    info('\n*** Testing Network #1\n')
    net.pingAll()

    info('\n*** Topology Morphing\n')    

    net.configLinkStatus("s1", "h9", "up")
    net.configLinkStatus("s2", "h9", "up")

    info( '*** Changing hosts default routes...\n')

    h1.cmd("ip route add default via 192.168.1.254")
    h2.cmd("ip route add default via 192.168.1.254")
    h3.cmd("ip route add default via 192.168.1.254")
    h4.cmd("ip route add default via 192.168.1.254")

    h5.cmd("ip route add default via 192.168.2.254")
    h6.cmd("ip route add default via 192.168.2.254")
    h7.cmd("ip route add default via 192.168.2.254")
    h8.cmd("ip route add default via 192.168.2.254")

    h9.cmd("ip route add 192.168.1.0 via 192.168.1.254")
    h9.cmd("ip route add 192.168.2.0 via 192.168.2.254")

    info('\n*** Testing Network #2\n')
    net.pingAll()


    

    CLI(net)
    net.stop() 


if __name__ == '__main__':
    setLogLevel( 'info' )
    defineNet()
