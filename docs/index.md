 ![Alt text](SimplyDomain-logo.png?raw=true "SimplyDomain")
Subdomain brute force focused on speed and data serialization. 
SimplyDomain uses a framework approach to build and deploy modules within. This allows
for fast, easy and concise output to feed into larger OSINT feeds.

## Demo
![GitHub Logo](https://github.com/SimplySecurity/SimplyDomain/blob/master/docs/sd-run.gif?raw=true)

## Installation
SimplyDomain is pure Python, and *should* support any platform. 
**Docker Install**
```bash
docker pull simplysecurity/simplydomain
```


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
dnsdumpster_search.py | Python API for Dnsdumpster | (Unofficial) Python API for https://dnsdumpster.com/ using @paulsec lib | 1.0
virus_total.py | Virus Total Subdomain Search | Uses https://virustotal.com search with unofficial search engine API support. | 1.0

## Running SimplyDomain 

```
root@kali:~# python3.6 SimplyDomain.py -h

    ------------------------------------------------------------
      ______  _______                                 __          
     /      \/       \                               /  |         
    /$$$$$$  $$$$$$$  | ______  _____  ____   ______ $$/ _______  
    $$ \__$$/$$ |  $$ |/      \/     \/    \ /      \/  /       \ 
    $$      \$$ |  $$ /$$$$$$  $$$$$$ $$$$  |$$$$$$  $$ $$$$$$$  |
     $$$$$$  $$ |  $$ $$ |  $$ $$ | $$ | $$ |/    $$ $$ $$ |  $$ |
    /  \__$$ $$ |__$$ $$ \__$$ $$ | $$ | $$ /$$$$$$$ $$ $$ |  $$ |
    $$    $$/$$    $$/$$    $$/$$ | $$ | $$ $$    $$ $$ $$ |  $$ |
     $$$$$$/ $$$$$$$/  $$$$$$/ $$/  $$/  $$/ $$$$$$$/$$/$$/   $$/ 
    ------------------------------------------------------------                                                                                              
    
usage: SimplyDomain.py [-h] [-m MODULE] [-o OUTPUT] [-on OUTPUT_NAME] [-l]
                       [-ll] [-v] [-d]
                       DOMAIN

positional arguments:
  DOMAIN                domain to query

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        module to hit
  -o OUTPUT, --output OUTPUT
                        output directory location (Ex. /users/test/)
  -on OUTPUT_NAME, --output-name OUTPUT_NAME
                        output directory name (Ex. test-2017)
  -l, --list            list loaded modules
  -ll, --long-list      list loaded modules and info about each module
  -v, --verbose         increase output verbosity
  -d, --debug           enable debug logging to .SimplyDns.log file, default
                        WARNING only
```

### Passive Collection
Using just the dynamic modules, SimplyDomain will not attempt to brute force any `A` records. You can easily run SimplyDomain via the virtual-env by using the `cd` command into the `SimplyDomain` dir. This will activate the python virtual environment and allow you to use python3.6 within.

```
python3.6 SimplyDomain.py test.com
```

### Active Collection
Enabling the wordlist brute force will allow you to discover new domains and attempt to brute force unknown or undiscovered domain names. Passing the `-wc` also allows you to specify up to the top 1 Million seen subdomains.

```
python3.6 SimplyDomain.py test.com -wb -wc 10000
```

### Output / Data Injector
All runs by default create a folder structure based on the domain name and time, this also includes:
* Grepable Text
* JSON Object
* Sorted Uniq Text File
* XML (In dev)

To change the location and output name use the following:

```
python3.6 SimplyDomain.py test.com -wb -wc 10000 -o /user/test/ -on foldername-to-pickup
```

## Contributing
This project is built with PyCharms and should be imported via the `.idea` Folder. Please make sure the following take place before submitting a pull request:

1. Passes all code `Inspections` - Python & General 
2. If possible unit tests of new code


