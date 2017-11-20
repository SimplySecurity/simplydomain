from src import core_serialization
from crtsh import crtshAPI
import json


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
        :return: 
        """
        queue_dict[]
        rd = []
        data = crtshAPI().search('uber.com')
        for d in data:
            rd.append(d)
        return rd