import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
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
            'Module': 'bing_search.py',

            # long name of the module to be used
            'Name': 'Bing Subdomain Search',

            # version of the module to be used
            'Version': '1.0',

            # description
            'Description': ['Uses Bing search engine',
                            'with unofficial search engine API support.'],

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI', '@ecjx'],

            # list of resources or comments
            'comments': [
                'https://github.com/ejcx/subdomainer/blob/master/subdomainer.py'
            ]
        }

        self.options = {

            'url': 'http://www.bing.com/search?q=site%3A%s&first=%s'
            'count'
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
        foundsubdomains = []
        core_args = self.json_entry['args']
        task_output_queue = queue_dict['task_output_queue']
        cs = core_scrub.Scrub()
        start_count = int(self.json_entry['bing_search']['start_count'])
        end_count = int(self.json_entry['bing_search']['end_count'])
        while start_count <= end_count:
            domain = "http://www.bing.com/search?q=site%3A" + \
                str(core_args.DOMAIN) + "&first=" + str(start_count)
            data, status = self.request_content(domain)
            soup = BeautifulSoup(data, 'html.parser')
            for i in soup.find_all('a', href=True):
                possiblesubdomain = i['href']
                if "." + str(core_args.DOMAIN) in possiblesubdomain:
                    parsed = urlparse(possiblesubdomain)
                    if parsed.netloc not in foundsubdomains:
                        foundsubdomains.append(str(parsed.netloc))
                    if parsed.hostname not in foundsubdomains:
                        foundsubdomains.append(str(parsed.hostname))
            for sub in foundsubdomains:
                cs.subdomain = sub
                # check if domain name is valid
                valid = cs.validate_domain()
                # build the SubDomain Object to pass
                sub_obj = core_serialization.SubDomain(
                    self.info["Name"],
                    self.info["Module"],
                    self.options['url'],
                    domain,
                    time.time(),
                    sub,
                    valid
                )
                task_output_queue.put(sub_obj)
                # results inc at rate of 10 per page
            start_count += 10
            time.sleep(0.5)
