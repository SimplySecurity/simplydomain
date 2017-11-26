import os
import random
import queue

from twisted.names import client
from src import core_serialization
from src import module_helpers


from src import core_scrub


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
            'Authors': ['@Killswitch-GUI'],

            # list of resources or comments
            'comments': [
                'Searches and performs recursive dns-lookup.'
            ],
            # priority of module (0) being first to execute
            'priority': 0
        }

        self.options = {
        }
        # ~ queue object
        self.word_list_queue = queue.Queue(maxsize=0)

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
        core_args = self.json_entry['args']
        core_resolvers = self.json_entry['resolvers']
        task_output_queue = queue_dict['task_output_queue']
        self._populate_word_list_queue()
        self._execute_resolve()
        cs = core_scrub.Scrub()

    def _populate_word_list_queue(self):
        """
        Populates word list queue with words to brute
        force a domain with.
        :return: NONE
        """
        word_count = int(self.json_entry['args'].wordlist_count)
        file_path = os.path.join(*self.json_entry['subdomain_bruteforce']['top_1000000'])
        with open(file_path) as myfile:
            # fancy iter so we can pull out only (N) lines
            sub_doamins = [next(myfile).strip() for x in range(word_count)]
        for sub in sub_doamins:
            self.word_list_queue.put(sub)

    def _select_random_resolver(self):
        """
        Select a random resolver from the JSON config, allows
        for procs to easily obtain a IP.
        :return: STR: ip
        """
        ip = random.choice(self.json_entry['resolvers'])
        return ip

    def _execute_resolve(self):
        """
        Executes a single threaded process Twisted DNS resolver,
        uses a queue to pop from stack.
        :return: NONE
        """
        # pop a word off Q object
        sub_word = self.word_list_queue.get()
        url = sub_word + '.' + self.json_entry['args'].DOMAIN
        test_url = 'ride.uber.com'
        # create resolver object, set hosts to NULL to prevent local lookup
        resolver_ip = self._select_random_resolver()
        print(resolver_ip)
        resolver = client.createResolver(servers=[(resolver_ip, 53)])
        d = resolver.getHostByName(test_url)
        input()
        print(d.result)

