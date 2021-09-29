# Lian_Yu (10.10.180.69)

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
21
22
80
111
```

## Users


```
vigilante:!#th3h00d -> creds for ftp
slade:M3tahuman -> creds for ssh
```


## Endpoints
```
/island
/island/2100
```


## Notes

* Found some endpoints using gobuster and one of them told me that the secret word was `vigilante`

* After that I found another endpoint (`/island/2100`) with an embed youtube video and in the source code I got a hint told me I needed to find a `.ticket` file

![image](https://user-images.githubusercontent.com/12052283/135309189-3b502517-84e3-4fd0-87f7-b6dada0fdabe.png)

* After this I tried to fuzz for a `.ticket` file in that directory using `gobuster dir -u http://10.10.180.69/island/2100 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x .ticket` and found `/green_arrow.ticket`

![image](https://user-images.githubusercontent.com/12052283/135312485-a5990a17-2caa-4428-aa14-14dd27380223.png)

* After a while I found that the `RTy8yhBQdscX` was a base58 hash. So after decoding I got `!#th3h00d`. Then I found that `vigilante:!#th3h00d` were the ftp creds

* Inside the ftp were 3 image files. I tried to use `steghide` but nothing worked. I needed a password for the `aa.jpg`

* `Leave_me_alone.png` was missing the header so I could not open it

* I tried to download every bash file and I noticed a `.other_user` file. This file only had a story line about Slade Wilson

* After a while, I decided to analyse the `Leave_me_alone.png` along with the `Queens_Gambit.png` since both are `.png` and one was opening and the other wasnt. Using `xxd` I found that the first file got a bad file signature so I needed to change that 

![image](https://user-images.githubusercontent.com/12052283/135317117-4a14bf99-2521-459f-9c68-bc91144a4e02.png)

* Using `xxd` I did the following to correct the file signature

 > `xxd Leave_me_alone.png hexdump`

 > `changed the HEX values comparing to the correct file signature of Queens_Gambit.png`

 > `xxd -r hexdump Leave_me_alone_good.png`

* Then I used `steghide extract -sf aa.jpg` and used the password that was inside `Leave_me_alone_good.png` 

* Unziping the output from steghide, got two files, `passwd.txt` and `shado` 

![image](https://user-images.githubusercontent.com/12052283/135319099-e3238a33-a74d-4ee5-b316-4e18be9c8c2e.png)

* So after this I found slade's creds to ssh

![image](https://user-images.githubusercontent.com/12052283/135320857-95517907-6de9-40ff-87b2-057860739213.png)

* Doing `sudo -l` looked like I could execute `pkexec` has sudo so I navigated to gtfobins and got root

![image](https://user-images.githubusercontent.com/12052283/135321374-f88895b8-b59f-48c1-9e09-ffd0642ebbd0.png)


# References

* https://crypto.bi/base58/

* https://stackoverflow.com/questions/58150200/how-to-change-file-header-in-terminal