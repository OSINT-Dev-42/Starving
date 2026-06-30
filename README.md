# Starving
Project to visualize changement of Google Maps review stars.

# Install python dependencies
```bash
pip install -r requirements.txt
playwright install --with-deps
```

# Configure Tor
```bash
sudo apt install tor # install tor
sudo systemctl start tor # start tor
# tor listens now on socks5://127.0.0.1:9050

sudo visudo # add the following line to the end of the file:
# your_username ALL=(root) NOPASSWD: /usr/sbin/service tor restart
```