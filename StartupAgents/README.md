# PyMonitorMQTT
## Windows
1. Edit Windows/PyMonitorMQTT.vbs to point to the right path to the project.
2. Copy PyMonitorMQTT.vbs file from Windows folder.
2. Open "shell:startup" or "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup".
3. Paste that file here.

## Linux with Systemd

You can run this program in the background automatically on startup this way.

1. Edit `StartupAgents/Linux/PyMonitorMQTT.service`
  
  - Change path on `ExecStart` line to point to main.py
    
  - Change user and group
    

2. Copy the unit file, than enable and start the daemon

```bash
sudo cp PyMonitorMQTT.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable PyMonitorMQTT.service
sudo systemctl start PyMonitorMQTT.service
```

3. Check if it's running correctly:

```bash
systemctl status PyMonitorMQTT.service
```

To check the logs:

```bash
sudo journalctl -u PyMonitorMQTT.service
```