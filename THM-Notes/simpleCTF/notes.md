# simpleCTF

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.117.82 -v`

`gobuster dir -u 10.10.117.82 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
21
80
2222
```

## Users


```
admin@admin.com:mitch:0c01f4468bd75d55:secret -> creds for ssh
```

## Endpoints
```
http://10.10.117.82/simple
http://10.10.117.82/simple/admin/login.php
```



## Vuln

```
CVE-2019-9053 SQL Injection in Exploit-db
```


## Notes

* Got port 80 open with apache2 default page

* Executing gobuster found `/simple` directory with CMS Made Simple v 2.2.8

* Found that CMS Made Simple v2.2.8 is vuln to CVE-2019-9053 SQL Injection in Exploit-db

* Using the script from exploit-db I was able found creds

![image](https://user-images.githubusercontent.com/12052283/130361185-3e222b8a-174b-487f-95e6-abfc21126534.png)

* Got `mitch` ssh creds and when running `sudo -l` I found `mitch` could run `vim without password`

* Went to gtfobins and got privesc using the vim binary

![image](https://user-images.githubusercontent.com/12052283/130366391-f953ee5b-4634-42d1-903d-db005cd1a6c3.png)


# References

* https://gtfobins.github.io/gtfobins/vim/
