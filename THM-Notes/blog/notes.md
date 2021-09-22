# Blog

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
22
80
139 -> smb
445 -> smb
```

## Users


```
bjoel -> wordpress user
kwheel:cutiepie1 -> wordpress user
```


## Endpoints

```

```



## Notes

* Found SMB share with public read and write access containing some files

![image](https://user-images.githubusercontent.com/12052283/134378904-7df77ae7-56b9-4a3c-b7ec-83866955a034.png)

* Connected into SMB using `smbclient  \\\\10.10.4.235\\BillySMB` and downloaded the 3 files

* Only one file was cool, a QRCode image but after decoding we I got nothing special, just another trool

![image](https://user-images.githubusercontent.com/12052283/134381693-283d6128-69e3-49f0-9fb8-f0df7cb24a6a.png)

* Runned WPscan and the found that the website is using `WordPress version 5.0 identified (Insecure, released on 2018-12-06)`

* Found two users `bjoel` and `kwheel` using `wpscan --url http://10.10.4.235/ -e u` and since XML-RPC is enabled I tried to bruteforce the login with both users doing `wpscan --url http://10.10.4.235/ -P /usr/share/wordlists/rockyou.txt -U users.txt -t 75` and only found `kwheel` password

* Started msfconsole and typed `searchsploit wordpress core 5.0` since I saw I could use this script to get a shell . Then I typed `search crop image` and used the first exploit and got a shell

![image](https://user-images.githubusercontent.com/12052283/134386528-aa109673-882a-4738-8ed5-cb1f3a0b4bee.png)

![image](https://user-images.githubusercontent.com/12052283/134387820-f5b77fd1-98ea-4028-b4e1-42127bdf6521.png)

* Then I upgraded from msfconsole to a normal shell using `shell` and then `script -qc /bin/bash /dev/null`

* Found a pdf file in `/home/bjoel` talking about his bad behaviour and tried to find `user.txt` with `find / 2>/dev/null | grep user.txt` ... but still could not find any way to get the user flag

* Found `/media/usb` but only `bjoel` and `root` where able to cd into 

* Runned linPEAS and found some database creds and `-rwsr-sr-x 1 root root 8.3K May 26  2020 /usr/sbin/checker (Unknown SUID binary)` . This binary is interesting because is not common and it was created in May 26 , the same month and day the box was created

![image](https://user-images.githubusercontent.com/12052283/134391051-8428dee1-de69-449f-b47d-9bc74fe159cc.png)

* Manual way to find SUID and SGIDs

> `find / -perm -u=s -type f 2>/dev/null`

> `find / -xdev -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null`

* Running the binary shows this 

![image](https://user-images.githubusercontent.com/12052283/134392121-10f3e43d-54a5-4c05-9900-6835a801d646.png)

* So I tried to run `ltrace checker` and I found that if an environment variable called `admin` was set to anything the binary assumes I am the admin, so I did that and I got root

![image](https://user-images.githubusercontent.com/12052283/134392418-6b3ec4e5-4f16-4b62-9f7a-97081a9d990b.png)

![image](https://user-images.githubusercontent.com/12052283/134392607-ddb97d8f-219f-448f-b309-aac3065f0131.png)

* Since I was root , I navigated to `/media/usb` and got the user flag too

* Decompiling `main` with `Ghidra` to see how the binary works

![image](https://user-images.githubusercontent.com/12052283/134394857-892804a6-3d2b-44d3-894a-cf4a5e4f1d17.png)


# References

* https://www.exploit-db.com/exploits/46662

* https://man7.org/linux/man-pages/man1/ltrace.1.html

* https://unix.stackexchange.com/questions/180867/how-to-search-for-all-suid-sgid-files