sudo apt update
sudo apt upgrade -y

sudo apt install -y python3-pip

sudo pip install pyserial

# influxdata-archive_compat.key GPG Fingerprint: 9D539D90D3328DC7D6C8D3B9D8FF8E1F7DF8B07E
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install -y influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb

sudo pip install influxdb

sudo apt install -y python3-pandas

sudo apt install -y openssh-server
sudo systemctl is-enabled ssh
sudo ufw allow ssh
sudo ufw enable
sudo ufw reload

curl -s https://install.zerotier.com | sudo bash
sudo zerotier-cli join 565799d8f62ca619

sudo usermod -a -G dialout global

sudo apt remove -y brltty

