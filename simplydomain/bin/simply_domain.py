#!/usr/bin/python3.6
import argparse
import json
import logging
import os
import sys

from simplydomain.src import core_printer
from simplydomain.src import core_runtime

from simplydomain.src import module_resolvers
from simplydomain.src import core_logger

# import json config..
from simplydomain import config


def _raw_depth_check(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value)
    if ivalue >= 6:
        raise argparse.ArgumentTypeError(
            "%s is too large of a keyspace for raw depth" % value)
    return ivalue


def cli_parse():
    """
    Parse the CLI args passed to the script.
    :return: args
    """
    # required
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
                        action="store", default=3, type=_raw_depth_check)
    parser.add_argument("-m", "--module", help="module to hit",
                        action="store")
    parser.add_argument(
        "-o", "--output", help="output directory location (Ex. /users/test/)")
    parser.add_argument("-on", "--output-name",
                        help="output directory name (Ex. test-2017)",)
    parser.add_argument("-l", "--list", help="list loaded modules",
                        action="store_true")
    parser.add_argument("-ll", "--long-list", help="list loaded modules and info about each module",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug logging to .SimplyDns.log file, default WARNING only",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("[!] verbosity turned on")
    return args, parser


def load_config(pr):
    """
    Loads .config.json file for use
    :return: dict obj
    """
    json_file = config.__json_config
    ds = module_resolvers.DnsServers()
    ds.populate_servers()
    json_file = ds.populate_config(json_file)
    print(pr.blue_text('Public DNS resolvers populated: (SERVER COUNT: %s)' %
                       (str(ds.count_resolvers()))))
    return json_file


def main():
    """
    Print entry screen and pass execution to CLI, 
    and task core.
    :return: 
    """
    pr = core_printer.CorePrinters()
    pr.print_entry()
    args, parser = cli_parse()
    logger = core_logger.CoreLogging()
    pr.print_config_start()
    config = load_config(pr)
    config['args'] = args
    if args.debug:
        pr.print_green_on_bold('[!] DEBUGGING ENABLED!')
        logger.start(logging.DEBUG)
    else:
        logger.start(logging.INFO)
    logger.infomsg('main', 'startup')
    if args.module:
        if not args.DOMAIN:
            parser.print_help()
        config['silent'] = False
        c = core_runtime.CoreRuntime(logger, config)
        c.execute_mp()
    elif args.list:
        c = core_runtime.CoreRuntime(logger, config)
        c.list_modules()
    elif args.long_list:
        c = core_runtime.CoreRuntime(logger, config)
        c.list_modules_long()
    else:
        if not args.DOMAIN:
            parser.print_help()
        config['silent'] = False
        c = core_runtime.CoreRuntime(logger, config)
        c.execute_mp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
