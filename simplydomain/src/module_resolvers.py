from fake_useragent import UserAgent
import json

from . import module_helpers


class DnsServers(module_helpers.RequestsHelpers):

    """
    A set of functions to find resolvers to use
    of high quality.
    """

    def __init__(self):
        """
        Init class structure.
        """
        module_helpers.RequestsHelpers.__init__(self)
        self.ua = UserAgent()
        self.nameservers = []
        self.nameserver_ips = []

    def populate_servers(self):
        """
        Populate server list.
        :return: NONE
        """
        data, status = self.request_json(
            'https://public-dns.info/nameserver/us.json')
        if status:
            data = json.loads(data)
            for d in data:
                self.nameservers.append(d)
        self.clean_servers()

    def populate_config(self, json_config):
        """
        Populate the json config file at runtime with
        public dns servers.
        :param json_config: start JSON config
        :return: json_config: final JSON config
        """
        json_config['resolvers'] = self.nameserver_ips[0:10]
        return json_config

    def clean_servers(self):
        """
        Sort name servers.
        :return: NONE
        """
        for i in self.nameservers:
            # check for 100% reliability
            if i['reliability'] == 1:
                self.nameserver_ips.append(i['ip'])

    def count_resolvers(self):
        """
        Count resolvers.
        :return: INT nameserver list count
        """
        return len(self.nameserver_ips)
