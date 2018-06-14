import time

from crtsh import crtshAPI
from simplydomain.src import core_serialization
from simplydomain.src import module_helpers

from simplydomain.src import core_scrub


class DynamicModule(object):
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
        self.json_entry = json_entry
        self.info = {
            # mod name
            'Module': 'crtsh_search.py',

            # long name of the module to be used
            'Name': 'Comodo Certificate Fingerprint',

            # version of the module to be used
            'Version': '1.0',

            # description
            'Description': ['Uses https://crt.sh search',
                            'with unofficial search engine support.'],

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI', '@PaulSec'],

            # list of resources or comments
            'comments': [
                'SHA-1 or SHA-256 lookup.'
            ]
        }

        self.options = {
            # threads for the module to use
            'Threads': 1
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

        :return: 
        """
        core_args = self.json_entry['args']
        task_output_queue = queue_dict['task_output_queue']
        cs = core_scrub.Scrub()
        rd = []
        data = crtshAPI().search(str(core_args.DOMAIN))
        for d in data:
            cs.subdomain = d['issuer']
            # check if domain name is valid
            valid = cs.validate_domain()
            # build the SubDomain Object to pass
            sub_obj = core_serialization.SubDomain(
                self.info["Name"],
                self.info["Module"],
                "https://crt.sh",
                self.info["Version"],
                time.time(),
                d['issuer'],
                valid
            )
            # populate queue with return data objects
            task_output_queue.put(sub_obj)
