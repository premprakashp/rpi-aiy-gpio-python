# GPIO Handler for Raspberry Pi to control mpd channels

## Copy systemd service to run on boot

```bash
sudo cp mpdgpio.service /lib/systemd/system/mpdgpio.service
sudo chmod 644 /lib/systemd/system/mpdgpio.service
sudo systemctl daemon-reload
sudo systemctl enable mpdgpio.service
sudo reboot
```
