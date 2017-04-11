sudo apt-get install python-dev
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
sudo python setup.py install
cd .. && rm -Rf SPI-Py
sudo pip install peewee python-ntlm pi-rc522
echo "dtparam=spi=on" >> /boot/config.txt
echo "dtoverlay=spi-bcm2708" >> /boot/config.txt