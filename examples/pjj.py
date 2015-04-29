#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
 
class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."
   def __init__(self, fanout=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""
 
       super(LinearTopo, self).__init__(**opts)
       cswitch = self.addSwitch('c1')
       for i in irange(1,fanout):
            aswitch = self.addSwitch('a%s' % i)
            self.addLink(cswitch,aswitch)
            for j in irange((i-1)*fanout+1,i*fanout):
                eswitch = self.addSwitch('e%s' % j)
                self.addLink(aswitch,eswitch,)
                for k in irange((j-1)*fanout+1,j*fanout):
                    host = self.addHost('h%s' % k)
                    self.addLink(eswitch,host)     
def perfTest():
   "Create network and run simple performance test"
   topo = LinearTopo(fanout=2)
   net = Mininet(topo)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   print "Testing bandwidth between h1 and h2"
   h1, h2 = net.get('h1', 'h2')
   net.iperf((h1, h2))
   
   print "Testing bandwidth between h1 and h4"
   h1, h4 = net.get('h1', 'h4')
   net.iperf((h1, h4))
   
   print "Testing bandwidth between h1 and h6"
   h1, h6 = net.get('h1', 'h6')
   net.iperf((h1, h6))
   net.stop()
 
if __name__ == '__main__':
   setLogLevel('info')
   perfTest()
