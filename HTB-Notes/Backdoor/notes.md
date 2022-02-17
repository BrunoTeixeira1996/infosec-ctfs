# Backdoor

* Found a wordpress site in port 80 (wp - 5.8.1)

* Running wpscan (`wpscan --url http://backdoor.htb --api-token B1lsJ5fSYNvdbsmOIYOrFa5vme57H1M2dsEFXNzOfs4 --enumerate p,u --plugins-detection aggressive`) I found akismet plugin (`Title: Akismet 2.5.0-3.1.4 - Unauthenticated Stored Cross-Site Scripting (XSS)`) -> `http://backdoor.htb/wp-content/plugins/akismet/`

* Going to `http://backdoor.htb/wp-content/plugins/akismet/` and backing up 1 dir I got this

![image](https://user-images.githubusercontent.com/12052283/154503342-5a8ced91-ecba-4908-91a0-6b9e16c47394.png)

* So I googled `ebook-downloads exploit` and got this https://www.exploit-db.com/exploits/39575 , so looks like a Directory Traversal Vuln

* Doing `http://backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../../wp-config.php` I was able to download `wp-config.php` file

```php
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpressuser' );

/** MySQL database password */
define( 'DB_PASSWORD', 'MQYBJSaD#DxG6qbm' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );
```


* I had no idea how to go from LFI to RCE ... but after a while I found this blog https://www.netspi.com/blog/technical/web-application-penetration-testing/directory-traversal-file-inclusion-proc-file-system/ on how can I abuse the proc file system using `/proc/PID/cmdline` -> `Lists everything that was used to invoke the process. This sometimes contains useful paths to configuration files as well as usernames and passwords.`

* So I decided to make a small python script to help me brute force the PID (`exploit.py`) and even using burp I found a service running in port 1337

![image](https://user-images.githubusercontent.com/12052283/154516143-db7cceb2-322c-4f17-94f8-20c2c01d58f8.png)

* Searching for gdb server in google , found this https://www.exploit-db.com/exploits/50539

* After a while I was not able to run the script so I used https://www.rapid7.com/db/modules/exploit/multi/gdb/gdb_server_exec/

* Got user.txt and moved to linpeas

* After running linpeas I saw `screen` and that was odd so I runned pspy to check for any cronjobs


![image](https://user-images.githubusercontent.com/12052283/154527412-f7940bb5-c94d-40ca-890c-554255c63b38.png)

* So screen is executing a cronjob that runs sleep, lets see if I can exploit this

* Tried using an exploit for screen 4.5.0 but we are running 4.08.0

* The other idea was to attach to the existing session since that session is running as root

* So using `screen -x root/root` I was able to be root