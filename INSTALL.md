# Installation Notes

* Burn an SD card from a Rapberry Pi OS (32-bit) image

* Boot and configure; recommendations:
  * **Wired network**, wifi okay for testing
  * **Static IP** or statically assigned DHCP
  * **Local timezone** (logs easier to parse)

* Further configuration: `sudo raspi-config`
  * Set hostname: System Options --> Hostname
  * Enable SSH: Interface Options --> SSH
  * Disable graphical interface: System Options --> Boot / Auto Login --> Console
    * Optional, but recommended for production

* Update system
```
sudo apt-get update
sudo apt-get upgrade
```

* Install prerequisites
```
sudo apt-get install apache2
```

* Create trax user
```
sudo useradd -d /home/trax -s /bin/bash -m trax
sudo usermod -G gpio trax
```

* Fetch trax code
```
cd /home/trax
sudo -u trax git clone https://github.com/vmoa/trax-pi.git
```

* Clean up stuff that should be part of a trax setup script
```
sudo touch /tmp/trax.lock 
sudo chmod 666 /tmp/trax.lock 
sudo touch /var/log/trax.log
sudo chown trax /var/log/trax.log
#
sudo cp /home/trax/trax-pi/static/index.html /var/www/html/
sudo cp /home/trax/trax-pi/static/trex-clipart.png /var/www/html/
#
sudo cp /home/trax/trax-pi/static/trax.service /etc/systemd/system/
sudo systemctl enable trax.service
sudo systemctl start trax.service
```

* RFO specific stuff
  * Add an admin user or two with SSH credentials (TODO)
  * Configure static route for VPN (TODO)

* Point a browser at your system and verify!

* Reboot and verify auto-start
```
sudo reboot
```

* Debugging commands if things go south
```
systemctl status trax.service
systemctl list-units | grep trax
journalctl -u trax.service
```
