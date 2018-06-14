import os
import random
import queue
import asyncio
import aiodns
import functools
import uvloop
import socket
import click
import time
import string
from tqdm import tqdm
from itertools import product

from simplydomain.src import core_serialization
from simplydomain.src import module_helpers
from simplydomain.src import core_scrub


# use RequestsHelpers() class to make requests to target URL
class DynamicModule(module_helpers.RequestsHelpers):
    """
    Dynamic module class that will be loaded and called
    at runtime. This will allow modules to easily be independent of the
    core runtime.
    """

    def __init__(self, json_entry):
        """
        Init class structure. Each module takes a JSON entry object which
        can pass different values to the module with out changing up the API.
        adapted form  Empire Project:
        https://github.com/EmpireProject/Empire/blob/master/lib/modules/python_template.py

        :param json_entry: JSON data object passed to the module.
        """
        module_helpers.RequestsHelpers.__init__(self)
        self.json_entry = json_entry
        self.info = {
            # mod name
            'Module': 'subdomain_bruteforce.py',

            # long name of the module to be used
            'Name': 'Recursive Subdomain Bruteforce Using Wordlist',

            # version of the module to be used
            'Version': '1.0',

            # description
            'Description': ['Uses lists from dnspop',
                            'with high quality dns resolvers.'],

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI', '@blark'],

            # list of resources or comments
            'comments': [
                'Searches and performs recursive dns-lookup.',
                ' adapted from https://github.com/blark/aiodnsbrute/blob/master/aiodnsbrute/cli.py'
            ],
            # priority of module (0) being first to execute
            'priority': 0
        }

        self.options = {
        }
        # ~ queue object
        self.word_count = int(self.json_entry['args'].raw_depth)
        self.word_list_queue = queue.Queue(maxsize=0)
        self.tasks = []
        self.domain = ''
        self.errors = []
        self.fqdn = []
        self.sub_gen_count = 0
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()
        self.resolver = aiodns.DNSResolver(loop=self.loop, rotate=True)
        # TODO: make max tasks defined in config.json
        self.max_tasks = 1024
        # TODO: make total set from wordcount in config.json
        self.sem = asyncio.BoundedSemaphore(self.max_tasks)
        self.cs = core_scrub.Scrub()
        self.core_args = self.json_entry['args']
        self.core_resolvers = self.json_entry['resolvers']
        self.silent = self.json_entry['silent']

    def dynamic_main(self, queue_dict):
        """
        Main entry point for process to call.

        core_serialization.SubDomain Attributes:
            name: long name of method
            module_name: name of the module that performed collection
            source: source of the subdomain or resource of collection
            module_version: version from meta
            source: source of the collection
            time: time the result obj was built
            subdomain: subdomain to use
            valid: is domain valid

        :return: NONE
        """
        self.task_output_queue = queue_dict['task_output_queue']
        self.domain = str(self.core_args.DOMAIN)
        self._execute_resolve()

    async def _process_dns_wordlist(self):
        """
        Populates word list queue with words to brute
        force a domain with.
        :return: NONE
        """
        # fancy iter so we can pull out only (N) lines
        sub_doamins = []
        for x in range(1, self.word_count+1, 1):
            sub_doamins += [''.join(i) for i in product(
                string.ascii_lowercase + string.digits, repeat=x)]
        self.sub_gen_count = len(sub_doamins)
        # move pbar here to ensure we have proper count at start
        if not self.silent:
            self.pbar = tqdm(total=self.sub_gen_count,
                             unit="records", maxinterval=0.1, mininterval=0)
        for word in sub_doamins:
            # Wait on the semaphore before adding more tasks
            await self.sem.acquire()
            host = '{}.{}'.format(word.strip(), self.domain)
            task = asyncio.ensure_future(self._dns_lookup(host))
            task.add_done_callback(functools.partial(
                self._dns_result_callback, host))
            self.tasks.append(task)
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def _select_random_resolver(self):
        """
        Select a random resolver from the JSON config, allows
        for procs to easily obtain a IP.
        :return: STR: ip
        """
        ip = random.choice(self.json_entry['resolvers'])
        return ip

    def _execute_resolve(self, recursive=True):
        """
        Execs a single thread based / adapted from:
        https://github.com/blark/aiodnsbrute/blob/master/aiodnsbrute/cli.py
        :return: NONE
        """
        try:
            self.logger("Brute forcing {} with a maximum of {} concurrent tasks...".format(
                self.domain, self.max_tasks))
            self.logger("Wordlist loaded, brute forcing {} DNS records".format(
                self.sub_gen_count))
            # TODO: enable verbose
            if recursive:
                self.logger("Using recursive DNS with the following servers: {}".format(
                    self.resolver.nameservers))
            else:
                domain_ns = self.loop.run_until_complete(
                    self._dns_lookup(self.domain, 'NS'))
                self.logger(
                    "Setting nameservers to {} domain NS servers: {}".format(self.domain, [host.host for host in domain_ns]))
                self.resolver.nameservers = [
                    socket.gethostbyname(host.host) for host in domain_ns]
                #self.resolver.nameservers = self.core_resolvers
            self.loop.run_until_complete(self._process_dns_wordlist())
        except KeyboardInterrupt:
            self.logger("Caught keyboard interrupt, cleaning up...")
            asyncio.gather(*asyncio.Task.all_tasks()).cancel()
            self.loop.stop()
        finally:
            self.loop.close()
            # TODO: enable verbose
            if not self.silent:
                self.pbar.close()
            self.logger(
                "completed, {} subdomains found.".format(len(self.fqdn)))
        return self.fqdn

    def logger(self, msg, msg_type='info', level=0):
        """A quick and dirty msfconsole style stdout logger."""
        # TODO: enable verbose
        if not self.silent:
            style = {'info': ('[*]', 'blue'), 'pos': ('[+]', 'green'), 'err': ('[-]', 'red'),
                     'warn': ('[!]', 'yellow'), 'dbg': ('[D]', 'cyan')}
            if msg_type is not 0:
                decorator = click.style('{}'.format(
                    style[msg_type][0]), fg=style[msg_type][1], bold=True)
            else:
                decorator = ''
            m = " {} {}".format(decorator, msg)
            tqdm.write(m)

    async def _dns_lookup(self, name, _type='A'):
        """Performs a DNS request using aiodns, returns an asyncio future."""
        response = await self.resolver.query(name, _type)
        return response

    def _dns_result_callback(self, name, future):
        """Handles the result passed by the _dns_lookup function."""
        # Record processed we can now release the lock
        self.sem.release()
        # Handle known exceptions, barf on other ones
        if future.exception() is not None:
            try:
                err_num = future.exception().args[0]
                err_text = future.exception().args[1]
            except IndexError:
                self.logger("Couldn't parse exception: {}".format(
                    future.exception()), 'err')
            if (err_num == 4):  # This is domain name not found, ignore it.
                pass
            elif (err_num == 12):  # Timeout from DNS server
                self.logger("Timeout for {}".format(name), 'warn', 2)
            elif (err_num == 1):  # Server answered with no data
                pass
            else:
                self.logger('{} generated an unexpected exception: {}'.format(
                    name, future.exception()), 'err')
            self.errors.append({'hostname': name, 'error': err_text})
        # Output result
        else:
            self.cs.subdomain = name
            # check if domain name is valid
            valid = self.cs.validate_domain()
            # build the SubDomain Object to pass
            sub_obj = core_serialization.SubDomain(
                self.info["Name"],
                self.info["Module"],
                "",
                self.info["Version"],
                time.time(),
                name,
                valid
            )
            self.task_output_queue.put(sub_obj)
            ip = ', '.join([ip.host for ip in future.result()])
            self.fqdn.append((name, ip))
            # self.logger("{:<30}\t{}".format(name, ip), 'pos')
            # self.logger(future.result(), 'dbg', 3)
        self.tasks.remove(future)
        # TODO: enable verbose
        if not self.silent:
            self.pbar.update()
