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
#sfrom nullswitch import NullSwitch

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

def defineNet():

    "Create a star network "

    net = Mininet( controller = RemoteController, waitConnected=True  )


    info( '*** Adding controller\n' )
    c0 = net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip="192.168.1.100/16")
    h2 = net.addHost( 'h2', cls=LinuxRouter, ip="192.168.2.100/16")
    h3 = net.addHost( 'h3', ip = "192.168.3.100/16")

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )

    info( '*** Creating hosts-switch links\n' )
    net.addLink( h1, s1) #, intfName2='s1-eth0', params2={ 'ip' : "192.168.1.1/16})"""
    net.addLink( h2, s1) #, intfName2='s1-eth1', params2={ 'ip' : "192.168.2.1/16" })""" 
    net.addLink( h3, s1) #, intfName2='s1-eth2', params2={ 'ip' : "192.168.3.1/16" })""" 
    

    info( '*** Starting network\n')
    net.start()

    info( '*** Hosts connections:\n')
    dumpNodeConnections(net.hosts)
    info( '\n')
    net.pingAll()

    info( '\n\n**** Topology Morphing ****\n\n')

    info( '*** Stopping hosts-switch connections...\n')
    net.configLinkStatus("h1", "s1", "down")
    net.configLinkStatus("h2", "s1", "down")
    net.configLinkStatus("h3", "s1", "down")

    info( '*** Creating new hosts-router links...\n' )
    net.addLink( h1, h2, intfName1='h1-eth1', intfName2='h2-eth1', params1={'ip' : "192.168.1.101/24"}, params2={'ip' : "192.168.1.1/24"} ) #params1={'ip' : '192.168.1.101/16'}, params2={ 'ip' : "192.168.1.2/16" })
    net.addLink( h3, h2, intfName1='h3-eth1', intfName2='h2-eth2', params1={'ip' : "192.168.3.101/24"}, params2={'ip' : "192.168.3.1/24"})#, intfName1='h3-eth1', params1={'ip' : '192.168.3.101/16'}, intfName2='h2-eth2', params2={ 'ip' : "192.168.3.2/16" })
    
    info( '*** Changing hosts default routes...\n')
    h1.cmd("ip route add default via 192.168.1.1")
    h3.cmd("ip route add default via 192.168.3.1")
    h2.cmd("ip route add 192.168.1.0 via 192.168.1.1")
    h2.cmd("ip route add 192.168.3.0 via 192.168.1.3")

    info('\n*** h2 routing table:\n')
    info( net[ 'h2' ].cmd( 'route' ) )


    info( '*** Hosts connections\n')
    dumpNodeConnections(net.hosts)
    net.pingAll()
    #info( '*** Running CLI\n' )
    #CLI( net )
    
    info( '\n*** Stopping network\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    defineNet()