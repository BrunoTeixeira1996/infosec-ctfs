# Pickle Rick


  <!--

    Note to self, remember username!

    Username: R1ckRul3s

  -->

## Scanning (`sudo nmap -sC -sV -oN nmap/initial 10.10.49.161`)

```
22
80
```



## Questions and Answers

* First ingredient (`mr. meeseek hair` found in /portal.php doing `less` in Sup3rS3cretPickl3Ingred.txt)

* Second ingredient (`1 jerry tear` found in /portal.php doing `ls -la /home/rick | less /home/rick/"second ingredients"`)

* Third ingredient (`fleeb juice` found in /portal.php doing `sudo less /root/3rd.txt`)


## Found Creds
* Username and Password (`R1ckRul3s`:`Wubbalubbadubdub` for 10.10.10.49.161/login.php found in robots.txt)

## Hints

* `less` works in 10.10.49.161/porta.php but `cat` dont
* `sudo -l` shows we can run any command using sudo without password (`(ALL) NOPASSWD: ALL`)
