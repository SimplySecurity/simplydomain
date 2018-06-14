[![Build Status](https://travis-ci.org/SimplySecurity/simplydomain-pkg.svg?branch=master)](https://travis-ci.org/SimplySecurity/simplydomain-pkg)
[![codebeat badge](https://codebeat.co/badges/981ba393-f661-47d1-95dc-6aa5a3c87e2c)](https://codebeat.co/projects/github-com-simplysecurity-simplydomain-master)
[![Maintainability](https://api.codeclimate.com/v1/badges/1da5e6c1c347559b6710/maintainability)](https://codeclimate.com/github/SimplySecurity/simplydomain/maintainability) 
 ![Alt text](simplydomain/docs/SimplyDomain-logo.png?raw=true "SimplyDomain")
#### Table of Contents 
---
- [simplydomain-pkg](#simplydomain-pkg)
  * [Three Core Design Principals:](#three-core-design-principals-)
- [Install simplydomain](#install-simplydomain)
  * [Using PIP Package Managment](#using-pip-package-managment)
  * [Using `setup.py` to build from source](#using--setuppy--to-build-from-source)
  * [simplydomain CLI tools (Quickstart)](#simplydomain-cli-tools--quickstart-)
  * [Install via Docker](#install-via-docker)
- [simplydomain programming API](#simplydomain-programming-api)
  * [Importing simplydomain into your project](#importing-simplydomain-into-your-project)
  * [Executing a search](#executing-a-search)
    + [simplydomain.execute_search(domain)](#simplydomainexecute-search-domain-)
    + [simplydomain.execute_raw_bruteforce(domain)](#simplydomainexecute-raw-bruteforce-domain-)
    + [simplydomain.execute_wordlist_bruteforce(domain)](#simplydomainexecute-wordlist-bruteforce-domain-)

# simplydomain-pkg 
Subdomain brute force focused on speed and data serialization. 
SimplyDomain uses a framework approach to build and deploy modules within. This allows
for fast, easy and concise output to feed into larger OSINT feeds.

## Three Core Design Principals:
* Easy install - support as many *NIX* based platforms.
* Pure Python - no other arbitrary setup processes and Python-3 support
* Expose public API - allows for simplydomain to integrate into other toolsets.

# Install simplydomain
You have a few fundamental choices when installing simplydomain; you can use your host systems python install, you can use `virtualenv` to ensure maximum capability, or Docker to have a clean environment.

## Using PIP Package Managment
```python
pip3 install simplydomain
```
or 
```python
python3 -m pip install simplydomain
```
## Using `setup.py` to build from source
```bash
git clone git@github.com:SimplySecurity/simplydomain-pkg.git | cd simplydomain-pkg
python3 -m pip install
```
## simplydomain CLI tools (Quickstart)
simplydomain supports a `bin` directory which is installed during the Python Setup PKG install. This now allows users to use their terminal of choice to use simplydomain.

To display Help:
```bash
simply_domain.py -h 
```
To run a basic passive sub-domain search:
```bash
simply_domain.py -all uber.com
```

## Install via Docker
The developed `Dockerfile` provides you with an easy way to spin up an instance and gain results in a short period without breaking certain dependencies. I highly suggest you use docker Volumes to ensure data persistence:

```bash
docker run -ti simplysecurity/simplydomain -h
```

# simplydomain programming API 
The simplydomain Python package allows you to expose a few critical areas of simplydomain to enable you easily extend or implement simplydomain in existing projects. 

*For reference the exposed API lives at https://github.com/SimplySecurity/simplydomain-pkg/simplydomain/__init__.py*

## Importing simplydomain into your project
Since simplydomain really at the core is a suite of high-level functions, there are only a few **High Level** API calls that can be made. For this reason, the exposed api is purely functioning vs. Class structures.
```python 
import simplydomain

simplydomain.<function>()
```
## Executing a search
simplydomain consists of many `Dynamic` modules and `Static` modules too allow a programmer to search a large subset of sources for subdomains easily. Within the simplydomain API, this concept is broken down into executing a large scale search function, and specific `Static` modules.

----
### simplydomain.execute_search(domain)
Executes the main search function(s) of simplydomain.

**Required Parameters**:
* domain (str) - sets the domain to search sub-domains for

**Optional Parameters**:
* config (dict) - sets the JSON config settings
* dnsservers (list) - sets a list of DNS servers for resolving Questions
* debug (bool) - sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
* verbose (bool) - set to enable verbose console messaging
* wordlist_bruteforce (bool) - sets to enable wordlist bruteforcing
* wordlist_count (bool) - top sub-domains count to bruteforce (1-1000000)
* raw_bruteforce (bool) - set to enable to brute force keyspace
* raw_depth (int) - depth to brute force keyspace (1-5)
* return_type (str) - (dict || json)

**Implemented Definition**  
```python
simplydomain.execute_search(
        domain,
        config={},
        dnsservers=[],
        debug='CRITICAL', 
        verbose=False, 
        wordlist_bruteforce=True, 
        wordlist_count=100,
        raw_bruteforce=True,
        raw_depth=3,
        return_type='json',
        ):
```

**Example(s)**
```python
>>> import simplydomain
>>> simplydomain.execute_search()
```

----
### simplydomain.execute_raw_bruteforce(domain)
Executes the static raw brute-force module of simplydomain. This allows simplydomain to generate all applicable RFC character sets off a subdomain keyspace. This can range from 1 char() to 5 char() which can feasibly be brute forced.

**Required Parameters**:
* domain (str) - sets the domain to search sub-domains for

**Optional Parameters**:
* config (dict) - sets the JSON config settings
* dnsservers (list) - sets a list of DNS servers for resolving Questions
* debug (bool) - sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
* verbose (bool) - set to enable verbose console messaging
* wordlist_bruteforce (bool) - sets to enable wordlist bruteforcing
* wordlist_count (bool) - top sub-domains count to bruteforce (1-1000000)
* raw_bruteforce (bool) - set to enable to brute force keyspace
* raw_depth (int) - depth to brute force keyspace (1-5)
* return_type (str) - (dict || json)

**Implemented Definition**  
```python
simplydomain.execute_raw_bruteforce(
        domain,
        config={},
        dnsservers=[],
        debug='CRITICAL', 
        verbose=False, 
        wordlist_count=0,
        return_type='json',
        wordlist_bruteforce=False,
        raw_bruteforce=True,
        raw_depth=2
        ):
```

**Example(s)**
```python
>>> import simplydomain
>>> simplydomain.execute_raw_bruteforce('uber.com', raw_depth=3)

'{"args": {"debug": true, "domain": "uber.com",..}, "data":...."}'
```

----
### simplydomain.execute_wordlist_bruteforce(domain)
Executes the static wordlist brute-force module of simplydomain. This allows simplydomain to get a range() of X subdomains for to be brute-forced. This can range from 1-1 Million words.

**Required Parameters**:
* domain (str) - sets the domain to search sub-domains for

**Optional Parameters**:
* config (dict) - sets the JSON config settings
* dnsservers (list) - sets a list of DNS servers for resolving Questions
* debug (bool) - sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
* verbose (bool) - set to enable verbose console messaging
* wordlist_bruteforce (bool) - sets to enable wordlist bruteforcing
* wordlist_count (bool) - top sub-domains count to bruteforce (1-1000000)
* raw_bruteforce (bool) - set to enable to brute force keyspace
* raw_depth (int) - depth to brute force keyspace (1-5)
* return_type (str) - (dict || json)

**Implemented Definition**  
```python
simplydomain.execute_raw_bruteforce(
        domain,
        config={},
        dnsservers=[],
        debug='CRITICAL', 
        verbose=False, 
        wordlist_count=100,
        return_type='json',
        wordlist_bruteforce=True,
        raw_bruteforce=False,
        raw_depth=0
        ):
```

**Example(s)**
```python
>>> import simplydomain
>>> simplydomain.execute_raw_bruteforce('uber.com', wordlist_count=100)

'{"args": {"debug": true, "domain": "uber.com",..}, "data":...."}'
```

