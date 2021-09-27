# Chill Hack

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
21 -> ftp
22 -> ssh
80 -> apache
```

## Users


```
user:password -> creds of what?
```


## Endpoints
```
/secret
```


## Notes

* Anonymous login in FTP is permited. Inside the FTP there is a `note.txt`

* Found `http://10.10.181.31/secret/` using gobuster. Inside this folder there is an input box that receives unix commands but does not accept any unix command. For instance, if I use `ls` there is something blocking

* Created the `bypass.py` exploit to automate this task.

* The simplest way that i always try to bypass any filtering in command injection is by using backslashes. So long as am not escaping any special characters then the word will still be interpreted the same way by bash

![image](https://user-images.githubusercontent.com/12052283/134927631-1293332e-00b9-42ef-9363-be588e2fc1af.png)

* After a while I saw that `nc, python, bash,php,perl,rm,cat,head,tail,python3,more,less,sh,ls` where forbidden words so I created a bash file in my computer that calls a reverse shell. After that I used the `bypass.py` to download that bash file and execute so I could get a reverse shell on the target machine

![image](https://user-images.githubusercontent.com/12052283/134933063-5b2c50d6-c6cd-4deb-a4cd-b83a9934746d.png)

* Doing `sudo -l` I see that user `www-data` can run `(apaar : ALL) NOPASSWD: /home/apaar/.helpline.sh` without password so I can escalate to `apaar` 

![image](https://user-images.githubusercontent.com/12052283/134938790-24095f5d-a2c7-4f16-8a31-16a42451b871.png)

* I found that port `9001` was being used so after I created a ssh connection back to `apaar` account I did a local forwarding with ssh tunneling using `ssh -L 9001:127.0.0.1:9001 -i apaar apaar@10.10.181.31`

![image](https://user-images.githubusercontent.com/12052283/134942391-c24625ef-74ae-4477-a23d-90fd4478fb01.png)


* To create the ssh connection I created a key using `ssh-keygen -f apaar` in my machine. Then I did `chmod 600 apaar` (changing erms in the priv key) , copied the pub key to the `.ssh/authorized_keys` file

* After the Local Forwarding I could go to `127.0.0.1:9001`

![image](https://user-images.githubusercontent.com/12052283/134941856-37d2becd-2868-4509-b557-cbac77f9d440.png)

* Searching a bit I found a file named `account.php` that has the logic for the login menu

![image](https://user-images.githubusercontent.com/12052283/134942964-fb355796-fd5d-478e-8464-2666f62a6efd.png)

* Since the code has 0 validation I bypassed the login using `'OR 1=1; --` because I could fail the username and password but the code gives a valid response if the input its true and 1=1 its true

![image](https://user-images.githubusercontent.com/12052283/134943432-37f30dcf-b15b-4b6d-bc62-0e28dbdc4a80.png)

* In `index.php` there are mysql creds in plaintext. Tried to login with root but got no success

![image](https://user-images.githubusercontent.com/12052283/134943725-edea2df6-f3b2-4211-9cf1-680d98eb5f18.png)

* After a while I tried to download `hacker-with-laptop_23-2147985341.jpg` and see if there is anything hiding

* Used `steghide extract -sf hacker-with-laptop_23-2147985341.jpg` and got a `backup.zip` . After that I used `zip2john backup.zip > zip.hash` to create a hash to use in john. Then I executed `john --wordlist=/usr/share/wordlists/rockyou.txt zip.hash` and got `pass1word`.

* Using `pass1word` to open the `backup.zip` got me a `source_code.php` file with `anurodh` ssh creds

![image](https://user-images.githubusercontent.com/12052283/134946902-7af3f8cd-ab6f-4dba-acd2-bb1d2d46bd6d.png)

* Using `id` I see that `anurodh` is in a docker group. Searching in gtfobins I saw a way to priv esc to root

![image](https://user-images.githubusercontent.com/12052283/134947493-f59f6206-1c58-47dc-82cf-a9829d59260c.png)


# References

* https://musyokaian.medium.com/chill-hack-walkthrough-tryhackme-498aa9ad1388