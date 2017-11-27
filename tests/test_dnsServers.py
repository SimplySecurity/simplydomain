from unittest import TestCase
from src import module_resolvers


class TestDnsServers(TestCase):

    m = module_resolvers.DnsServers()
    m.populate_servers()

    def test_populate_servers(self):
        a = self.m.nameserver_ips
        if '8.8.8.8' not in a:
            self.fail("missing google resolver in list!")

    def test_populate_config(self):
        j = {}
        j = self.m.populate_config(j)
        if '8.8.8.8' not in j['resolvers']:
            self.fail('resolver json missing google')

    def test_clean_servers(self):
        self.m.clean_servers()
        if not self.m.nameserver_ips:
            self.fail()

    def test_count_resolvers(self):
        if self.m.count_resolvers() < 1:
            self.fail('no resolvers populated')
