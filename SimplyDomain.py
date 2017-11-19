#!/usr/bin/python3
import os
import sys
import argparse
import logging
from src import core_printer
from src import core_runtime
from src import core_logger


def cli_parse():
    """
    Parse the CLI args passed to the script.
    :return: args
    """
    # required
    parser = argparse.ArgumentParser()
    parser.add_argument("DOMAIN", help="domain to query")
    # opts
    parser.add_argument("-m", "--module", help="module to hit",
                        action="store")
    parser.add_argument("-l", "--list", help="list loaded modules",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug logging to .SimplyDns.log file, default WARNING only",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("[!] verbosity turned on")
    return args


def main():
    """
    Print entry screen and pass execution to CLI, 
    and task core.
    :return: 
    """
    pr = core_printer.CorePrinters()
    pr.print_entry()
    args = cli_parse()
    logger = core_logger.CoreLogging()
    if args.debug:
        logger.start(logging.DEBUG)
    logger.infomsg('main', 'startup')
    if args.module:
        print()
    elif args.list:
        c = core_runtime.CoreRuntime(logger)
        c.list_modules()
    else:
        c = core_runtime.CoreRuntime(logger)
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