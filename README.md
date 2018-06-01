 [![Build Status](https://travis-ci.org/SimplySecurity/SimplyDomain.svg?branch=master)](https://travis-ci.org/SimplySecurity/SimplyDomain)
  [![Coverage Status](https://coveralls.io/repos/github/SimplySecurity/SimplyDomain/badge.svg?branch=master)](https://coveralls.io/github/SimplySecurity/SimplyDomain?branch=master)
 ![Alt text](docs/SimplyDomain-logo.png?raw=true "SimplyDomain")

 
# SimplyDomain
Subdomain brute force focused on speed and data serialization. 
SimplyDomain uses a framework approach to build and deploy modules within. This allows
for fast, easy and concise output to feed into larger OSINT feeds.

[INSTALL / FAQ]
https://simplysecurity.github.io/SimplyDomain/

[CHANGELOG]
https://github.com/SimplySecurity/SimplyDomain/blob/master/CHNAGELOG.md

[HELP/QUESTIONS/CHAT] Join us at: https://simplysecurity.herokuapp.com

### TL;DR
#### Via cURL
```bash
root@kali:~# curl -s https://raw.githubusercontent.com/SimplySecurity/SimplyDomain/master/setup/oneline-setup.sh | bash
root@kali:~# cd SimplyDomain
root@kali:~/SimplyDomain# ./SimplyDomain.py
```
#### Via Docker
```bash
docker pull simplysecurity/simplydomain
docker create -v ~/.simplydomain:/opt/data/ --name sd-data simplysecurity/simplydomain
docker run --volumes-from sd-data -ti simplysecurity/simplydomain -h
```
