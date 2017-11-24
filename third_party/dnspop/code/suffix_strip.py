#!/usr/bin/env python3

# Strip suffixes from domains using data from the Public Suffix List
# For background see: https://bitquark.co.uk/blog/2016/02/29/the_most_popular_subdomains_on_the_internet
# (c)oded 2015-∞ Jon - bitquark.co.uk

import sys
import os.path
import multiprocessing

def strip_domain(domain):
    """ Strip a domain of its suffix """
    domain = domain.rstrip()
    for suffix in suffixes:
        if domain.endswith(suffix):
            return domain[:-len(suffix)]

# Check that the public suffix list exists
if not os.path.isfile('public_suffix_list.dat'):
    sys.exit('[!] No suffix list found. You can download the latest copy from: https://publicsuffix.org/list/')

# Build a list of domain suffixes using the public suffix list from publicsuffix.org
# Note that the file is read backwards to prevent, .uk superceding .co.uk, for example
with open('public_suffix_list.dat') as fh:
    public_suffixes = [('.' + line.replace('*.', '')) for line in reversed(fh.readlines()) if line[0:2] != '//' and line[0] != '!' and line != '\n']

# Domains with > 400k records in the 2016-02-13 Project Sonar Forward DNS data set and which
# don't supercede sub-TLD parts (e.g. .jp is excluded because of .ne.jp, .co.jp, etc)
common_suffixes = [ '.com', '.net', '.ne.jp', '.de', '.org', '.edu', '.nl', '.info', '.biz', '.co.uk', '.cz', '.dk',
                    '.com.cn', '.mil', '.ac.uk', '.ch', '.eu', '.com.br', '.co.za', '.ad.jp', '.ac.cn', '.com.au',
                    '.or.jp', '.net.au', '.asia', '.ac.jp', '.mobi', '.co.jp', '.sk', '.edu.tw', '.net.pl', '.gov' ]

# Create the suffix list
suffixes = common_suffixes + [_.rstrip() for _ in public_suffixes if _.rstrip() not in common_suffixes]

# Create a multiprocessing pool and iterate over domains
pool = multiprocessing.Pool()
with sys.stdin as fh:
    for domain in pool.imap(strip_domain, fh, 1024):
        print(domain)

