sudo useradd -d /home/trax -s /bin/bash -m trax
sudo usermod -G gpio trax

# These should be fixed in code or startup script
sudo chmod 666 /tmp/trax.lock 
sudo touch /var/log/trax.log
sudo chown trax /var/log/trax.log

sudo cp static/trax.service /etc/systemd/system/
sudo systemctl enable trax.service
sudo systemctl start trax.service
systemctl status trax.service
systemctl list-units | grep trax
journalctl -u trax.service
