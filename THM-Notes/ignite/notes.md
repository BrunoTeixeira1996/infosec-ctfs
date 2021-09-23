# Ignite

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
80
```

## Users


```
admin:admin -> creds of http://10.10.209.51/fuel/
```


## Endpoints
```
http://10.10.209.51/fuel
```


## Notes

* Found that port 80 was running Fuel CMS version 1.4 with defaults creds in `/fuel` 

* Found CVE-2018-16763 about Fuel CMS and got RCE using `searchsploit -x linux/webapps/47138.py`

* Got rev shell using `exploit.py` as user `www-data`

* Using `find / -xdev -type f -name flag.txt 2>/dev/null` found the `flag.txt`

* Found root creds in `/var/www/html/fuel/application/config/database.php` and got the `root.txt`


# References

* https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-16763