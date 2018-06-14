from simplydomain.src import core_printer
from simplydomain.src import core_runtime
from simplydomain.src import module_resolvers
from simplydomain.src import core_logger

# import json config..
from simplydomain import config

import os
import sys
import json
import logging
import argparse

##### SIMPLYDOMAIN API FUNCTIONS #####

# STATICS
__core_printer = core_printer.CorePrinters()
__core_logger = core_logger.CoreLogging()
__core_dns_servers = module_resolvers.DnsServers()

"""
Current JSON config struc:
wordlist_bruteforce: BOOL
wordlist_count: INT
raw_bruteforce: BOOL
raw_depth: INT
verbose: BOOL
debug: BOOL
"""


def __raw_depth_check(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value)
    if ivalue >= 6:
        raise argparse.ArgumentTypeError(
            "%s is too large of a keyspace for raw depth" % value)
    return ivalue


def __load_dns(config):
    __core_dns_servers.populate_servers()
    __core_dns_servers.populate_config(config)


def __load_config():
    return config.__json_config


def __set_logging(value):
    """
    sets the logging function outlet.
    """
    if value == 'CRITICAL':
        __core_logger.start(logging.CRITICAL)
    if value == 'ERROR':
        __core_logger.start(logging.ERROR)
    if value == 'WARNING':
        __core_logger.start(logging.WARNING)
    if value == 'INFO':
        __core_logger.start(logging.INFO)
    if value == 'DEBUG':
        __core_logger.start(logging.DEBUG)


def __parse_values(
        domain,
        debug,
        verbose,
        wordlist_bruteforce,
        wordlist_count,
        raw_bruteforce,
        raw_depth
):
    parser = argparse.ArgumentParser()
    parser.add_argument("DOMAIN", help="domain to query")
    # opts
    parser.add_argument("-wb", "--wordlist-bruteforce", help="enable word list bruteforce module",
                        action="store_true")
    parser.add_argument("-wc", "--wordlist-count", help="set the count of the top words to use DEFAULT: 100",
                        action="store", default=100, type=int)
    parser.add_argument("-rb", "--raw-bruteforce", help="enable raw bruteforce module",
                        action="store_true")
    parser.add_argument("-rd", "--raw-depth", help="set the count of depth to raw bruteforce DEFAULT: 3",
                        action="store", default=3, type=__raw_depth_check)
    parser.add_argument("-m", "--module", help="module to hit",
                        action="store")
    parser.add_argument(
        "-o", "--output", help="output directory location (Ex. /users/test/)")
    parser.add_argument("-on", "--output-name",
                        help="output directory name (Ex. test-2017)",)
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug logging to .SimplyDns.log file, default WARNING only",
                        action="store_true")
    args = []
    if debug:
        args.append('-d')
    if verbose:
        args.append('-v')
    if wordlist_bruteforce:
        args.append('-wb')
    if wordlist_count:
        args.append('-wc')
        args.append(str(wordlist_count))
    if raw_bruteforce:
        args.append('-rb')
    if raw_depth:
        args.append('-rd')
        args.append(str(raw_depth))
    if domain:
        args.append(str(domain))
    return parser.parse_args(args)


def execute_raw_bruteforce(
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
    """
    executes the main search function of simplydomain:
    config: sets the JSON config settings for the opperation
    dnsservers: sets a list of top DNS servers to resolve.
    debug: sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    verbose: sets the verbose count
    wordlist_count: cound to brute 1-1000000
    return_type: (dict | json)
    """
    __set_logging(debug)
    if not config:
        config = __load_config()
    if not dnsservers:
        dnsservers = __load_dns(config)
    config['args'] = __parse_values(
        domain,
        debug,
        verbose,
        wordlist_bruteforce,
        wordlist_count,
        raw_bruteforce,
        raw_depth
    )
    cr = core_runtime.CoreRuntime(__core_logger, config)
    return cr.execute_raw_bruteforce(return_type=return_type)


def execute_wordlist_bruteforce(
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
    """
    executes the main search function of simplydomain:
    config: sets the JSON config settings for the opperation
    dnsservers: sets a list of top DNS servers to resolve.
    debug: sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    verbose: sets the verbose count
    wordlist_count: cound to brute 1-1000000
    return_type: (dict | json)
    """
    __set_logging(debug)
    if not config:
        config = __load_config()
    if not dnsservers:
        dnsservers = __load_dns(config)
    config['args'] = __parse_values(
        domain,
        debug,
        verbose,
        wordlist_bruteforce,
        wordlist_count,
        raw_bruteforce,
        raw_depth
    )
    cr = core_runtime.CoreRuntime(__core_logger, config)
    return cr.execute_bruteforce(return_type=return_type)


def execute_search(
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
    """
    executes the main search function of simplydomain:
    config: sets the JSON config settings for the opperation
    dnsservers: sets a list of top DNS servers to resolve.
    debug: sets the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    verbose: sets the verbose count
    wordlist_bruteforce: sets to use worlist brute static module
    wordlist_count: cound to brute 1-1000000
    raw_bruteforce: set to try to brute force keyspace
    raw_depth: set to 1-5
    return_type: (dict | json)
    """
    __set_logging(debug)
    if not config:
        config = __load_config()
    if not dnsservers:
        dnsservers = __load_dns(config)
    # now setup the config file
    # in JSON format for the core
    # to use within simplydomain
    config['args'] = __parse_values(
        domain,
        debug,
        verbose,
        wordlist_bruteforce,
        wordlist_count,
        raw_bruteforce,
        raw_depth
    )
    cr = core_runtime.CoreRuntime(__core_logger, config)
    return cr.execute_amp(return_type=return_type)
