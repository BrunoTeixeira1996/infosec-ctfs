# BountyHacker

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.11.100 -v`

`gobuster dir -u 10.10.11.100 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
22/tcp open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
80
```

## Users

```php
<?php
// TODO -> Implement login system with the database.
$dbserver = "localhost";
$dbname = "bounty";
$dbusername = "admin";
$dbpassword = "m19RoAU0hP41A1sTsq6K";
$testuser = "test";
?>
```

```
admin:m19RoAU0hP41A1sTsq6K -> database creds
development:m19RoAU0hP41A1sTsq6K -> ssh creds
```


## Endpoints
```
10.10.11.100/resources/README.txt -> [ ] Disable 'test' account on portal and switch to hashed password. Disable nopass
10.10.11.100/resources/bountylog.js -> tracker_diRbPr00f314.php
```



## Vuln


```
XXE in http://10.10.11.100/log_submit.php
```
![image](https://user-images.githubusercontent.com/12052283/127709897-e56f3206-b9ad-44a5-9828-f55cf44159a1.png)

![image](https://user-images.githubusercontent.com/12052283/127711550-07faee37-6037-4cf3-8e16-a4b8b910e639.png)

![image](https://user-images.githubusercontent.com/12052283/127711665-8742b8e0-692a-4ccc-a263-132dac6fb926.png)

![image](https://user-images.githubusercontent.com/12052283/127712202-21d3a5d2-dfd6-4c2d-87f6-86bede77979f.png)


```
User development can (root) NOPASSWD: /usr/bin/python3.8 /opt/skytrain_inc/ticketValidator.py
ticketValidator.py is vuln_file.py
```

![image](https://user-images.githubusercontent.com/12052283/127714461-369de778-1e42-4c25-87ca-f649a62efa12.png)

* Getting root from development

![image](https://user-images.githubusercontent.com/12052283/127715798-3d69cfa9-8e18-4de5-8153-360f67c421ab.png)


# References

* https://portswigger.net/web-security/xxe

* 