#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink, Intf

def topology():
    print("Create a network.")
    net = Mininet(controller=RemoteController)

    print ("*** Creating nodes")
    h1 = net.addHost('h1') # Client
    h2 = net.addHost('h2') # Client
    h3 = net.addHost('h3') # Client
    h4 = net.addHost('h4') # Server

    switches = []
    switches.append(net.addSwitch('s1', protocols=["OpenFlow13"]))
    switches.append(net.addSwitch('s2', protocols=["OpenFlow13"]))
    switches.append(net.addSwitch('s3', protocols=["OpenFlow13"]))
    switches.append(net.addSwitch('s4', protocols=["OpenFlow13"]))

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    print("*** Creating links")
    link_bw = {'bw':100}
    net.addLink(h1, switches[0], **link_bw)
    net.addLink(h2, switches[0], **link_bw)
    net.addLink(h3, switches[0], **link_bw)
    net.addLink(h4, switches[3], **link_bw)

    net.addLink(switches[0], switches[1], **link_bw)
    net.addLink(switches[0], switches[2], **link_bw)
    net.addLink(switches[3], switches[1], **link_bw)
    net.addLink(switches[3], switches[2], **link_bw)

    print("*** Starting network")
    net.build()
    c0.start()

    for sw in switches:
      sw.start([c0])

    # Speed up the emulation by using static ARP
    h1.cmd('arp -s '+ h4.IP() + ' ' + h4.MAC())
    h1.cmdPrint('arp -n')
    h2.cmd('arp -s '+ h4.IP() + ' ' + h4.MAC())
    h2.cmdPrint('arp -n')
    h3.cmd('arp -s '+ h4.IP() + ' ' + h4.MAC())
    h3.cmdPrint('arp -n')

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()

