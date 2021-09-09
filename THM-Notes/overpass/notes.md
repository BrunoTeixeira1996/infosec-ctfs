# Overpass

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
80
22
```

## Users


```
james:james13 -> creds for ssh
```


## Endpoints
```
/admin
```


## Notes

* Found a webserver and in the source code found this

![image](https://user-images.githubusercontent.com/12052283/132727810-ce8ff721-7a1a-4d77-8029-7915ea9fadd2.png)

* Using gobuster found `/admin`

* Found 3 js files but only `login.js` was good

![image](https://user-images.githubusercontent.com/12052283/132728976-926a3894-77b6-4b10-a3c1-cd30f876c59d.png)

* Looking at the function login there’s a simple if else statement. Basically, it’s checking if the response is equal to `"Incorrect Crentials"`. If true, it will display a message saying “Incorrect Credentials”. Otherwise, it will set a cookie named `“SessionToken”` to the returned statusOrCookie and redirect the user to `/admin`. Since this is only checking for a cookie named SessionToken I created the cookie with `SessionToken` name and got this. A RSA Private Key

![image](https://user-images.githubusercontent.com/12052283/132731073-b371c3a7-e2d9-407b-87cd-2ff51cbeb9b8.png)

* So I picked up the RSA Private Key, copy and paste to the `james_priv_key` file, `chmod 600` the file and `ssh -i priv_key james@10.10.44.128` but it asks for a passphrase and james password.

* After that I decided to use john to decrypt the Encrypted RSA , so I did `python /usr/share/john/ssh2john.py james_priv_key > james.hash` and then `john --wordlist=/usr/share/wordlists/rockyou.txt --format=SSH james.hash` to decrypt. John returned `james13` for the passphrase. Logged in with ssh and got the user.txt flag

* Running linPEAS got this

![image](https://user-images.githubusercontent.com/12052283/132736603-9f6f3f03-0739-4d00-8d81-2f24f0859e5b.png)


* Since its a cronjob that runs every minute localy I tricked the server to download from my machine a malicious file instead of downloading from 127.0.0.1 and then I got root.txt flag

![image](https://user-images.githubusercontent.com/12052283/132743195-475a203f-de19-42aa-be5b-72f82abec44a.png)



# References

* John Hammond