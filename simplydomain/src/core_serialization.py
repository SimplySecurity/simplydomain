import json


class SerializeJSON(object):

    """
    Core data handler for json output. Stores all final objects
    and allows a standard way to ingest data from SimplyDomain.

    Sample JSON Data Struc:

    JSON_OUTPUT = {
        "meta_data": {
            "version": 0.1,
            "author": "Alexander Rymdeko-Harvey",
            "twitter": "Killswitch-GUI",
            "github_repo": "https://github.com/killswitch-GUI/SimplyDomain"
        },


        "args": {
            "domain": "google.com",
            "verbose": false,
            "debug": false
        },

        "data": [
            {
                "name": "cert search",
                "module_name": "crtsh_search.py",
                "source": "github.com",
                "time": 1222121212.11,
                "subdomain": "test.test.com"
            },
            {
                "name": "cert search",
                "module_name": "crtsh_search.py",
                "source": "github.com",
                "time": 1222121212.11,
                "subdomain": "test.test.com"
            }
        ]
    }
    """

    def __init__(self, config):
        """
        Init class struc. Used as a object to parse and populate
        results.
        """
        self.subdomains = {}
        self.subdomains['args'] = {}
        self.subdomains['data'] = []
        self.subdomains['meta_data'] = config['meta_data']
        self.subdomains['args']['domain'] = config['args'].DOMAIN
        self.subdomains['args']['debug'] = config['args'].debug
        self.subdomains['args']['verbose'] = config['args'].verbose

    def add_subdomain(self, input_obj):
        """
        Add subdomain to class kbject for storage untill output is needed.
        :param input_obj: class object of subdomain
        :param config: core .config.json and params loaded
        :return: 
        """
        subdomain = {}
        subdomain['name'] = input_obj.name
        subdomain['module_name'] = input_obj.module_name
        subdomain['module_version'] = input_obj.module_version
        subdomain['source'] = input_obj.source
        subdomain['time'] = input_obj.time
        subdomain['toolname'] = input_obj.toolname
        subdomain['subdomain'] = input_obj.subdomain
        subdomain['valid'] = input_obj.valid
        self.subdomains['data'].append(subdomain)

    def print_json_subdomains(self):
        """
        Simple test print.
        :return: 
        """
        json_str = json.dumps(self.subdomains, sort_keys=True, indent=4)
        print(json_str)


class SubDomain(object):

    """
    Core data handler to clean, and post results in proper
    DataSerialization format for SimplyDomain.

    Attributes:
        name: long name of method
        module_name: name of the module that performed collection 
        source: source of the subdomain or resource of collection
        module_version: version from meta
        source: source of the collection
        time: time the result obj was built
        toolname: tool used to collect data
        subdomain: subdomain to use
        valid: is domain valid
    """

    def __init__(self, name, module_name, module_version, source, time, subdomain, valid):
        """
        Init class struc. Used as a object to parse and populate
        results.
        """
        self.name = name
        self.module_name = module_name
        self.module_version = module_version
        self.source = source
        self.time = time
        self.toolname = "SimplyDomain"
        self.subdomain = subdomain
        self.valid = valid
