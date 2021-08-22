# cyborg


## Open ports

```
80
22
```

## Users


```
music_archive:$apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.:squidward -> creds for borgbackup
alex:S3cretP@s3 -> creds for ssh
```


## Endpoints
```
http://10.10.47.172/etc/squid/squid.conf
http://10.10.47.172/etc/squid/passwd
```

## Notes

* Found website and when running gobuster found `squid` creds in `http://10.10.47.172/etc/squid/`

![image](https://user-images.githubusercontent.com/12052283/130371738-21fd71dc-bd5e-448a-87e5-ee416c1c9053.png)

* Cracked hash with hashcat using md5(apr) and found `squidward`

* Downloaded archive from website and since its using borgbackup, I installed borgbackup and extracted the backup using `borg extract final_archive::music_archive` and `squidward` has the password and found more creds for ssh

![image](https://user-images.githubusercontent.com/12052283/130371839-c5f3c5f2-6099-4f9e-ae7b-6b00158f7d5b.png)

* Doing `sudo -l` I can see that alex can run a backup script

![image](https://user-images.githubusercontent.com/12052283/130371860-20b0e28c-d728-4a16-b6f0-f7db0fce01d8.png)

* In this `while loop` I saw that it takes an command line argument and executes in the end of the backup, and since alex runs this backup has sudo I privesc

![image](https://user-images.githubusercontent.com/12052283/130371890-eb22524f-505e-480d-9ce6-ad36e6d074de.png)

![image](https://user-images.githubusercontent.com/12052283/130371930-42ce05b5-89d4-49eb-bdaf-fbb3bb13ebdd.png)


# References

* https://borgbackup.readthedocs.io/en/stable/installation.html

* https://borgbackup.readthedocs.io/en/stable/usage/extract.html