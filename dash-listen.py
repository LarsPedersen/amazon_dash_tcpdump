import subprocess as sub
from qhue import Bridge

b = Bridge("192.168.0.99", "username")
print b.url
print b.lights[1]()
 
p = sub.Popen(('sudo', 'tcpdump', '-e', '-i', 'eth0', 'arp', '-l'), stdout=sub.PIPE)
for line in iter(p.stdout.readline, b''):
  if line.rstrip().find("50:f5:da:ed:55:8f") >= 0:
    print "Found the Dash. " + line.rstrip()
    b.lights[1].state(on=False) 
