# DNSpop

Tools to find popular trends by analysis of DNS data. For more information, see my blog post on [the most popular subdomains on the internet](https://bitquark.co.uk/blog/2016/02/29/the_most_popular_subdomains_on_the_internet). Hit the results directory to get straight to the data.

## code/subpop.sh

A script to build a list of popular subdomains based on Rapid7's Project Sonar [Forward DNS](https://github.com/rapid7/sonar/wiki/Forward-DNS) data set.

## code/suffix_strip.py

A script to efficiently strip suffixes from domains using data from the [Public Suffix List](https://publicsuffix.org/list/). Used by _subpop.sh_ but can be used as a stand-alone script.

## results/*

Result sets from the above tools.
