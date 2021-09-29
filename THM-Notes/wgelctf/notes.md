# wgelctf (10.10.201.87)

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
22
80
```

## Users


```
jessie:id_rsa key -> creds for ssh
```


## Endpoints
```
/sitemap/
/sitemap/.ssh/
```



## Notes

* Found `apache` running and with a strange comment 

 > `<!-- Jessie don't forget to udate the webiste -->`

* Found a website in `/sitemap/` using `unapp template` from `colorlib`

* With `gobuster dir -u http://10.10.201.87/sitemap -w /usr/share/wordlists/dirb/common.txt` I found some interesting files

![image](https://user-images.githubusercontent.com/12052283/135326362-b6958bfb-ea5f-431a-87bc-6ee9c5a4750b.png)

* `sitemap/.ssh/` had a rsa key. After I download that key I did `chmod 600 id_rsa` to grant perms and tried to login with that rsa key using `ssh jessie@10.10.201.87 -i id_rsa` since `jessie` looked like a valid user name from the comment in the past

* And here I got the user flag

* Doing `sudo -l` I see that we can run `wget` has sudo so I can abuse that to escalate to root

![image](https://user-images.githubusercontent.com/12052283/135327728-45da5907-1dea-49f0-a8c2-db5e65aece51.png)

* Parei aqui , falta abusar o wget


# References

* https://vk9-sec.com/wget-privilege-escalation/