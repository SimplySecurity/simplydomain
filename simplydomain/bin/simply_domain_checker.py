#!/usr/bin/python3.6


"""
SimplyDomainChecker.python
Author: Brad Crawford

Takes JSON input from SimplyDomain and resolves subdomain CNAMES
looking for possible subdomain takeover opportunities.

"""

import sys
import json
import argparse

from provider import PROVIDER_LIST
from simplydomain.src import module_checker


def lookup_cname(filename):


	print("\nLoaded {} providers from provider.py\n".format(len(PROVIDER_LIST)))


	#Open JSON file and build a list of domains marked as valid
	with open(filename) as json_file:
		json_data = json.load(json_file)
	json_list = json_data['data']	
	valid_domain_list = {obj['subdomain'] for obj in json_list if obj['valid']}
	print("\nLoaded {} unique domains\n".format(len(valid_domain_list)))
	
	myDns = module_checker.DnsChecker(valid_domain_list)
	pair_dict = myDns.run()
	for key,value in pair_dict.items():
		print("Subdomain: {} ||| CNAME: {}".format(key,value))
	#TODO: Add native HTTPS support

	myHttp = module_checker.HttpChecker(myDns.cname_results)
	output = myHttp.run()
	print(output)

def cli_parser():
	"""
	Parse the CLI args passed to the script.
	:return: args
	"""

	parser = argparse.ArgumentParser()
	# mandatory
	parser.add_argument("FILENAME", help="full path and filename")
	
	# optional

	args = parser.parse_args()
	return args

def main():
	args = cli_parser()
	lookup_cname(args.FILENAME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)