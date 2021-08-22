# Agent Sudo

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.19.248 -v`

`gobuster dir -u 10.10.19.248 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
21
22
80
```

## Users


```
chris:crystal -> creds for ftp
james:hackerrules! -> creds for ssh
```


## Endpoints
```

```



## Vuln


```
```

## Notes

* Found a webserver 

![image](https://user-images.githubusercontent.com/12052283/130366723-abf96128-1106-46d3-b2cc-c6778a2f9c58.png)

* The idea is to use burp and change the user-agent to access the page

![image](https://user-images.githubusercontent.com/12052283/130366894-e26d0810-5674-4a38-8916-e5a83d07df81.png)

* Burp did nothing but I assumed that 25 employes are a quote for the alphabet so I tried in curl and saw this

![image](https://user-images.githubusercontent.com/12052283/130367159-be33e5d8-a2b8-4789-af10-92416b911271.png)

* Using hydra I could bruteforce FTP password

![image](https://user-images.githubusercontent.com/12052283/130367310-6bc69d70-9336-42d1-8449-8dd94d2bbb39.png)


* Logging in ftp as chris I saw 3 files

![image](https://user-images.githubusercontent.com/12052283/130367389-713ff2da-7101-416b-82ad-c34b02626596.png)


* Reading this I was thinkin about using a steganography tool 

![image](https://user-images.githubusercontent.com/12052283/130367461-e8b9a03a-e903-4045-9561-fed03b038030.png)

![image](https://user-images.githubusercontent.com/12052283/130367977-d4260e01-df12-4e63-87be-d145a6238adc.png)

* Cracked zip file password using zip2john

![image](https://user-images.githubusercontent.com/12052283/130369644-3aa1400a-f04f-4215-9873-14df1bf653b1.png)

* Decoding the hash from text file and getting the correct passphrase for the steg

![image](https://user-images.githubusercontent.com/12052283/130369830-199db482-eab4-4d4f-8e60-d57d27ae9586.png)

![image](https://user-images.githubusercontent.com/12052283/130369875-735cd826-4321-4198-a1f6-703b3c1ead43.png)

* Privesc to root , first method

![image](https://user-images.githubusercontent.com/12052283/130370293-27c26295-e4c1-4256-83d6-87411def3786.png)

* Privesc to root, second method

![image](https://user-images.githubusercontent.com/12052283/130370346-3c79c7e9-54d2-4a30-98d9-79a3af042761.png)


# References

* https://book.hacktricks.xyz/linux-unix/privilege-escalation#users
