#!/bin/bash

# Build a list of popular subdomains based on Rapid7's Project Sonar Forward DNS data set
# For background see: https://bitquark.co.uk/blog/2016/02/29/the_most_popular_subdomains_on_the_internet
# DNS data from: https://github.com/rapid7/sonar/wiki/Forward-DNS
# Public suffix data from: https://publicsuffix.org/

# Hello!
echo "Subpop - (c)oded 2015-∞ Jon - bitquark.co.uk"

# Find the date of the most recent DNS data set
DATA_DATE=`ls -r1 ????????_dnsrecords_all 2>/dev/null | head -1 | cut -d _ -f 1`
if [ -z $DATA_DATE ]; then
	echo "[!] No DNS data found. You can download the latest data set from: https://scans.io/study/sonar.fdns"
	exit
fi
echo ".oO( Using DNS data from $DATA_DATE )"

# Retrieve suffixes from the publicsuffix.org list
echo ".oO( Updating public suffix list )"
curl -s https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat > public_suffix_list.dat

# Speeds things up considerably, and should be fine working with subdomains
# For info, see http://www.inmotionhosting.com/support/website/ssh/speed-up-grep-searches-with-lc-all
export LC_ALL=C

# The domain list contains records of all types (e.g. mx, txt, cname), let's de-dupe the list.
# With the 2015-06-06 data set this gets us from 1,421,085,853 (68G) records to 523,039,450 (13G)
# There are about 1.6k records that a 'sort -u' would remove but it's not really worth the extra processing time
echo ".oO( De-duping DNS records )"
pv $DATA_DATE"_dnsrecords_all" | cut -d , -f 1 | uniq > $DATA_DATE"_domains_with_tld"

# Strip TLDs from domains
# Some TLDs use extended characters, so we unset LC_ALL here
echo ".oO( Stripping TLDs )"
pv $DATA_DATE"_domains_with_tld" | LC_ALL= ./suffix_strip.py | grep '\.' | uniq > $DATA_DATE"_domains_without_tld"

# Take the left-most subdomain from each record and combine with the domain before running uniq to
# make sure that subdomains only get counted once per domain, then trim off the domain part
echo ".oO( Extracting subdomains )"
pv $DATA_DATE"_domains_without_tld" | awk -F . '{print $1 ":" $NF}' | uniq | cut -d : -f 1 | sort > $DATA_DATE"_subdomains_raw"

# Do the final tally of popular domains
echo ".oO( Tallying up and sorting by subdomain popularity )"
pv $DATA_DATE"_subdomains_raw" | uniq -c | sort -rn > $DATA_DATE"_subdomains_popular"

# Fin
echo "All done! Popular subdomains are in "$DATA_DATE"_subdomains_popular"

