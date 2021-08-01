# Explore

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.10.247 -v`

`sudo nmap -sC -sV -p- nmap/all 10.10.10.247 -v`

### Open ports

```
2222/tcp open     ssh     (protocol 2.0) SSH-2.0-SSH Server - Banana Studio
5555/tcp filtered freeciv

Discovered open port 37557/tcp on 10.10.10.247
59777/tcp open     http    Bukkit JSONAPI httpd for Minecraft game server 3.6.0 or older
```


## Notes

```
TCP port 5555 will immediately take your attention if you are a mobile security enthusiast. In fact, on Android, 5555 TCP port open usually means Android Debug Bridge Daemon(ADBD) listening over the network
```
* Android Debug Bridge Daemon is listening over the network (port 5555/tcp open)


connect -> `adb connect ip:port`

start server -> `sudo adb start-server`

kill server -> `sudo adb kill-server`

list devices -> `adb devices`

* Tried to connect using adb but nothing worked


* Found ES File Explorer Open Port Vulnerability - CVE-2019-6447 on port 59777 and got creds with that CVE

## Users


`kistri:Kr1sT!5h@Rp3xPl0r3!` -> creds found in `http://10.10.10.247:59777/storage/emulated/0/DCIM/creds.jpg` and got `user.txt` in `/mnt/sdcard/user.txt`




## Vuln

* ES File Explorer Open Port Vulnerability - CVE-2019-6447 - Getting device info

![image](https://user-images.githubusercontent.com/12052283/127781306-61ac034a-bc5e-4f60-9aaf-306bbc1d89f8.png)

* ES File Explorer Open Port Vulnerability - CVE-2019-6447 - Listing pics

![image](https://user-images.githubusercontent.com/12052283/127781443-c3737240-c417-4a4d-b2ba-8f1b69bb609b.png)

* ES File Explorer Open Port Vulnerability - CVE-2019-6447 - Got ssh creds

![image](https://user-images.githubusercontent.com/12052283/127781492-1606dea2-03f8-40f9-8a62-fc347a877acb.png)

* ES File Explorer Open Port Vulnerability - CVE-2019-6447 - Got user.txt with ssh creds

![image](https://user-images.githubusercontent.com/12052283/127781875-05e25f7b-43b1-47e2-a5d6-b5927f37f124.png)



## Getting root

* Starting `adb server` , local forwarding to 10.10.10.247 and redirecting trafic from local 5555 port to 10.10.10.247:5555 , then connecting with `adb connect` to localhost:5555 redirecting local trafic to 10.10.10.247:5555

![image](https://user-images.githubusercontent.com/12052283/127786400-41d4a04f-78bd-4489-a2bc-5f01ff627ab5.png)

* Inside shell , to escalate to sudo I only typed `su` and became `root` and then did `find . -type f -name root.txt 2>/dev/null` to find the root.txt flag

![image](https://user-images.githubusercontent.com/12052283/127786705-98ec6f2d-4a0f-4416-90dd-cc1c78d0ac1f.png)


# References

* https://labs.f-secure.com/blog/hackin-around-the-christmas-tree 

* https://portswigger.net/daily-swig/android-file-manager-app-exposing-user-data-through-open-port

* https://github.com/fs0c131y/ESFileExplorerOpenPortVuln

* https://www.safe.security/assets/img/research-paper/pdf/es-file-explorer-vulnerability.pdf

* https://serverfault.com/questions/1022710/ssh-local-forwarding

* https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding