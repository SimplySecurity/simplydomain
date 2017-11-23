Subdomain brute force focused on speed and data serialization. 
SimplyDomain uses a framework approach to build and deploy modules within. This allows
for fast, easy and concise output to feed into larger OSINT feeds.

## Installation
SimplyDomain is pure Python, and *should* support any platform. 

**One-line** install with bash:
```bash
root@kali:~# curl -s https://raw.githubusercontent.com/SimplySecurity/SimplyDomain/master/setup/oneline-setup.sh | bash
root@kali:~# cd SimplyDomain
(SD) root@kali:~/SimplyDomain# ./SimplyDomain.py
```

**Git clone** install with `setup.sh` which builds a Python virtual env:
```bash
root@kali:~# git clone https://github.com/SimplySecurity/SimplyDomain.git
root@kali:~# ./SimplyDomain/setup.sh
root@kali:~# cd SimplyDomain
(SD) root@kali:~/SimplyDomain# ./SimplyDomain.py
```

**Source** install with **no** Python virtual end:
```bash
root@kali:~# git clone https://github.com/SimplySecurity/SimplyDomain.git
root@kali:~# cd SimplyDomain/setup/
root@kali:~# pip install -r requirements.txt
root@kali:~# cd ..
root@kali:~# python3.6 SimplyDomain.py -h
```

### Install FAQ
* Python: Python 3.6 required
* OS: SimplyDomain is pure Python if it runs Python it should work
* Priv: Requires `sudo` to install

## Module Support

Module | Name | Description | Version
--- | --- | --- | ---
crtsh_search.py | Comodo Certificate Fingerprint | Uses https://crt.sh search with unofficial search engine support. | 1.0
bing_search.py | Bing Subdomain Search | Uses Bing search engine with unofficial search engine API support. | 1.0



## Contributing
This project is built with PyCharms and should be imported via the `.idea` Folder. Please make sure the following take place before submitting a pull request:

1. Passes all code `Inspections` - Python & General 
2. If possible unit tests of new code


