### A simple Amazon Dash Button Iot implementation for Raspberry Pi using Python and tcpdump.

Being intimidated by the rather high price of various wifi based Iot buttons, which was in the range of ..., I purchased a couple of Amazon Dash buttons in order to make a cheap Internet button for various Iot projects. One idea was to make a button at the main entrance that would turn off all lights when leaving home - just to get started.

I found the idea from [this Medium post by Edward Bensen](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.nmfbh834n), which uses the Python module scapy to detech when the Dash Button is pressed. The default mode of the Dash Button is to be completely turned off and when pressed it fires up and connects to the network. It does this by broadcasting an ARP message to the network to identify the network gateway. With the Python script and the [scapy](https://www.secdev.org/projects/scapy/) module it should be possible to detect ARP packages from the Dash Button Mac address.

However it was not possible to make the script run consistently on a Raspberry Pi 2. I tried many suggestions for making it work, amongst others this [ Amazon Dash Hack with the Raspberry Pi](https://github.com/vancetran/amazon-dash-rpi) but I was not able to install Python 2.7.9 - even trying this [Raspberry ressource](http://raspberrypi.stackexchange.com/questions/26286/update-python-version-on-raspbian). I also attempted this [Stack Exchange](http://unix.stackexchange.com/questions/223255/using-python-and-scapy-to-sniff-for-arp-on-pi) and this [Reddit thread] (https://www.reddit.com/r/homeautomation/comments/3gy2u7/help_with_python_and_scapy_amazon_button_on_pi/?) resources with similar suggestions but with tweaks.

Then I took another path and attempted to use tcpdump and the subprocess module. With the help of these threads [Handling tcpdump output in python](http://stackoverflow.com/questions/17904231/handling-tcpdump-output-in-python) and [Python: read streaming input from subprocess.communicate()](http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate/17698359#17698359) I was able to construct the following script. 

```python
import subprocess as sub
from qhue import Bridge

b = Bridge("192.168.0.99", "username")
print b.url
print b.lights[1]()

p = sub.Popen(('sudo', 'tcpdump', '-e', '-i', 'eth0', 'arp', '-l'), stdout=sub.$
for line in iter(p.stdout.readline, b''):
  if line.rstrip().find("50:f5:da:ed:55:8f") >= 0:
    print "Found the Dash. " + line.rstrip()
    b.lights[1].state(on=False)
```

The script was able to detect the ARP calls from the Dash Button every time, and the effort to assembly the script was small compared to the many hours I tried with the [scapy](https://www.secdev.org/projects/scapy/) approach.

The current state of the tcpdump script is that it works, but it is not fast. The input buffering seems not to work as explained in the resources mentioned above, so it does take some seconds before the lights are turned off. But it will do for now, as long as it is robust and I can count on that the lights are turned off every time, which seems to be the case.

I used the [Qhue](https://github.com/quentinsf/qhue) python script to talk to the Phillips Hue and this nice post for setting up a [cron job](http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/) that runs the script at start-up.
