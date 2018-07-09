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
import dns.resolver
from tqdm import tqdm

from simplydomain.src import core_serialization
from simplydomain.src import core_scrub
from simplydomain.src import module_helpers
from multiprocessing import Process


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
        self.word_count = int(self.json_entry['args'].wordlist_count)
        self.word_list_queue = queue.Queue(maxsize=0)
        self.tasks = []
        self.domain = ''
        self.errors = []
        self.fqdn = []
        self.runtime_queue = []
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()
        self.resolver = aiodns.DNSResolver(loop=self.loop, rotate=True)
        # TODO: make max tasks defined in config.json
        self.max_tasks = 500
        # TODO: make total set from wordcount in config.json
        self.sem = asyncio.BoundedSemaphore(self.max_tasks)
        self.cs = core_scrub.Scrub()
        self.core_args = self.json_entry['args']
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
        self.subdomain_list = queue_dict['subdomain_list']
        self.domain = str(self.core_args.DOMAIN)
        self._execute_resolve(self.domain)

    async def _process_dns_wordlist(self, domain):
        """
        Populates word list queue with words to brute
        force a domain with.
        :return: NONE
        """
        h = module_helpers.RequestsHelpers()
        content, ret = h.request_text(
            'https://github.com/bitquark/dnspop/raw/master/results/bitquark_20160227_subdomains_popular_1000000')
        if not ret:
            raise Exception(
                'Failed to request bitquark top_1000000 sub domains.')
        # file_path = os.path.join(*self.json_entry['subdomain_bruteforce']['top_1000000'])
        # fancy iter so we can pull out only (N) lines
        sub_doamins = content.split()
        #sub_doamins = [next(content).strip() for x in range(self.word_count)]
        for word in sub_doamins[0:self.word_count]:
            # Wait on the semaphore before adding more tasks
            await self.sem.acquire()
            host = '{}.{}'.format(word.strip(), domain)
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

    def _runtime_loop(self):
        """runtime time that allows recursive search
        """
        try:
            for x in self.runtime_queue:
                # the inital loop branch to control
                # the runtime of a search
                self._execute_resolve(x, exit=True)
                self.runtime_queue.remove(x)
            if self.runtime_queue:
                # only hit this branch if more values have
                # been added to the queue
                self._runtime_loop()
            else:
                # runtime completed
                return
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                self.logger("Caught keyboard interrupt, cleaning up...")
                asyncio.gather(*asyncio.Task.all_tasks()).cancel()
                self.loop.stop()
            except SystemExit:
                os._exit(0)

    def _execute_resolve(self, domain, recursive=True, exit=False):
        """
        Execs a single thread based / adapted from:
        https://github.com/blark/aiodnsbrute/blob/master/aiodnsbrute/cli.py
        :return: NONE
        """
        try:
            _valid = True
            self.logger("Brute forcing {} with a maximum of {} concurrent tasks...".format(
                domain, self.max_tasks))
            self.logger(
                "Wordlist loaded, brute forcing {} DNS records".format(self.word_count))
            if self._check_wildcard_domain(domain):
                self.logger("Core domain: {} is a wildcard DNS A record domain! Check yourself..".format(domain), msg_type='err')
                self.logger("Moving striaght to past subdomains", msg_type='err')
            # TODO: enable verbose
            if not self.silent:
                self.pbar = tqdm(total=self.word_count,
                                 unit="records", maxinterval=0.1, mininterval=0)
            if recursive:
                self.resolver.nameservers = self.json_entry['resolvers']
                self.logger("Using recursive DNS with the following servers: {}".format(
                    len(self.resolver.nameservers)))
            else:
                domain_ns = self.loop.run_until_complete(
                    self._dns_lookup(domain, 'NS'))
                self.logger(
                    "Setting nameservers to {} domain NS servers: {}".format(domain, [host.host for host in domain_ns]))
                self.resolver.nameservers = [
                    socket.gethostbyname(host.host) for host in domain_ns]
                #self.resolver.nameservers = self.core_resolvers
            self.loop.run_until_complete(self._process_dns_wordlist(domain))
        except KeyboardInterrupt:
            self.logger("Caught keyboard interrupt, cleaning up...")
            asyncio.gather(*asyncio.Task.all_tasks()).cancel()
            self.loop.stop()
        finally:
            # 
            # TODO: enable verbose
            if not self.silent:
                # 
                self.pbar.close()
                self.logger(
                    "completed, {} subdomains found.".format(len(self.fqdn)))
            if exit:
                # to prevent runtime loops from spawning
                return
            for x in self.subdomain_list:
                    if not self._check_wildcard_domain(x):
                        self.runtime_queue.append(x)
            if self.runtime_queue:
                self._runtime_loop()
            self.loop.close()
            self.pbar.close()
        return self.fqdn

    def logger(self, msg, msg_type='info'):
        """A quick and dirty msfconsole style stdout logger.
        
        Uses style decorator to print a console message that is tqdm safe and
        prevents the console bars from being altered. Only prints WHEN
        no silent is enabled.
        
        Arguments:
            msg {str} -- message you want to print
        
        Keyword Arguments:
            msg_type {str} -- sets color / style setting (default: {'info'})
        """
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

    def _check_wildcard_domain(sef, name, _type='A'):
        """check if domain A record is *.
        
        [description]
        
        Arguments:
            sef {[type]} -- [description]
            name {[type]} -- [description]
        
        Keyword Arguments:
            _type {str} -- [description] (default: {'A'})
        
        Returns:
            bool -- is domain wildcard domain A record.
        """
        x = "*.{}".format(name)
        try:
            answers = dns.resolver.query(x, _type)
            if answers:
                return True
        except Exception as e:
            pass
        return False

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
            if valid:
                if not self._check_wildcard_domain(name):
                    self.runtime_queue.append(name)
            self.task_output_queue.put(sub_obj)
            ip = ', '.join([ip.host for ip in future.result()])
            self.fqdn.append((name, ip))
            # self.logger("{:<30}\t{}".format(name, ip), 'pos')
            # self.logger(future.result(), 'dbg', 3)
        self.tasks.remove(future)
        # TODO: enable verbose
        if not self.silent:
            self.pbar.update()
