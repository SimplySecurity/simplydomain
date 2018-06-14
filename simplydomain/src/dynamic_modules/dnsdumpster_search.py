import time

from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
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
            'Module': 'dnsdumpster_search.py',

            # long name of the module to be used
            'Name': 'Python API for Dnsdumpster',

            # version of the module to be used
            'Version': '1.0',

            # description
            'Description': ['(Unofficial) Python API for',
                            'https://dnsdumpster.com/ using @paulsec lib.'],

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI', '@PaulSec'],

            # list of resources or comments
            'comments': [
                'Searches for prior seen domains, as well as data that goes with those.'
            ]
        }

        self.options = {

            'threads': '',
            'url': 'https://dnsdumpster.com',
        }

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
        task_output_queue = queue_dict['task_output_queue']
        cs = core_scrub.Scrub()

        data = DNSDumpsterAPI().search(str(core_args.DOMAIN))
        for d in data['dns_records']['host']:
            cs.subdomain = d['domain']
            # check if domain name is valid
            valid = cs.validate_domain()
            # build the SubDomain Object to pass
            sub_obj = core_serialization.SubDomain(
                self.info["Name"],
                self.info["Module"],
                self.options['url'],
                self.info["Version"],
                time.time(),
                d['domain'],
                valid
            )
            # populate queue with return data object
            task_output_queue.put(sub_obj)
