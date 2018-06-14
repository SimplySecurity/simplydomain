from unittest import TestCase
from src import core_printer


class TestCorePrinters(TestCase):
    p = core_printer.CorePrinters()

    def test_blue_text(self):
        msg1 = self.p.blue_text("test")
        msg2 = "\x1b[34m [*] \x1b[0mtest"
        self.assertEqual(msg1, msg2)

    def test_green_text(self):
        msg1 = self.p.green_text("test")
        msg2 = "\x1b[32m [+] \x1b[0mtest"
        self.assertEqual(msg1, msg2)

    def test_print_entry(self):
        self.p.print_entry()

    def test_print_d_module_start(self):
        self.p.print_d_module_start()

    def test_print_s_module_start(self):
        self.p.print_s_module_start()

    def test_print_config_start(self):
        self.p.print_config_start()

    def test_print_modules(self):
        self.p.print_modules(['modules/bing_search.py'])
