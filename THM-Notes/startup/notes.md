# Startup

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial [ip] -v`

`sudo nmap -p- nmap/allports [ip] -v`

`gobuster dir -u [ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`


### Open ports

```
Discovered open port 22/tcp on 10.10.50.195
Discovered open port 80/tcp on 10.10.50.195
Discovered open port 21/tcp on 10.10.50.195
```

## Users


```
lennie:c4ntg3t3n0ughsp1c3 -> creds of ssh
```


## Endpoints
```
/files
```



## Notes

* Found anonymous login in FTP

![image](https://user-images.githubusercontent.com/12052283/134034194-f6e47947-3627-4bd5-8dd8-396bb7a3ed7c.png)

* Since I could upload files inside the `ftp folder` I uploaded a shell and activate that shell in the `/files` endpoint

![image](https://user-images.githubusercontent.com/12052283/134041995-80a78df9-35d3-4ca1-af61-6685d1196ce1.png)

`python3 -c 'import pty;pty.spawn("/bin/bash")'`-> to fix the shell

* Found `/incidents` and inside that folder a file called `suspicious.pcapng`

* Looks like someone uploaded a webshell too

![image](https://user-images.githubusercontent.com/12052283/134045555-c3db373b-6771-4691-bafd-035da5a8c01f.png)

* And this pcapng file shows that exist a `recipe.txt` file that contains `lennie` creds

* In the pcapng file there are some TCP streams that show that someone was inside the box and tried to change user to www-data , and typed another password. That password belongs to user `lennie`

![image](https://user-images.githubusercontent.com/12052283/134048862-108ac7a5-0cf1-4002-9a21-3dbb136407f7.png)

* I found some files inside `scripts` folder. The `planner.sh` executes another file called `print.sh` . `print.sh` executes an echo but `planner.sh` is running has `root`, so I only needed to make a rev shell inside `print.sh` and execute `planner.sh` to escalate to root. But there is a catch, I cant simply run `planner.sh` has sudo or anything so I was hoping `planner.sh` was running has a cronjob, and it was.

![image](https://user-images.githubusercontent.com/12052283/134054277-fee2c519-4749-406c-a518-99e5ce8e8530.png)


![image](https://user-images.githubusercontent.com/12052283/134055717-e58c0f51-dc90-482c-98bc-f29476664a3e.png)

* Checking that there is a cronjob running has root with pspy64

![image](https://user-images.githubusercontent.com/12052283/134058659-d2fb02ed-e3bc-430d-a2ee-14ab5c4f2180.png)


* Getting root

![image](https://user-images.githubusercontent.com/12052283/134055851-3a04e30f-7086-4326-bf51-e0f2343b3162.png)


# References

* How to spy cronjobs

* Always disable anonymous ftp login