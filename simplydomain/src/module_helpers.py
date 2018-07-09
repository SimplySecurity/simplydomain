import requests
import validators
from fake_useragent import UserAgent

from . import core_output


class RequestsHelpers(core_output.CoreOutput):

    """
    A set of functions to make requests standard and handle fail cases 
    to prevent error msgs.
    """

    def __init__(self):
        """
        Init class structure.
        """
        # TODO: Init Logging class
        core_output.CoreOutput.__init__(self)
        self.ua = UserAgent()

    def get_dns_wildcard(self, domain):
        try:
            x = "*.{}".format(domain)
            url = 'https://dns.google.com/resolve?name=%s&type=A' % (str(x))
            headers = {"Accept": "application/json"}
            response = requests.get(url,headers=headers,verify=True)
            return response.json()
        except Exception as e:
            print(response.text)
            return {}

    # split up json from raw for future support
    def request_json(self, url, return_code=200):
        """
        Request JSON content and expected return code.
        :param url:  URL to request
        :param return_code: expected return code or raise error
        :return: JSON, SuccessState
        """
        try:
            header = {
                'User-Agent': str(self.ua.google)
            }
            if not validators.url(url):
                self.print_yellow(
                    " [!] Invalid URL Requested: %s" % (str(url)))
                return {}, False
            r = requests.get(url, headers=header)
            if r.status_code != return_code:
                self.print_yellow(" [!] Request returned invalid status code: (CODE): %s (EXPECTED): %s" %
                                  (str(r.status_code), str(return_code)))
                return {}, False
            return r.content, True
        except requests.ConnectTimeout as e:
            self.print_red(
                " [!] Request ConnectionTimeout: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.TooManyRedirects as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.HTTPError as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except ConnectionError as e:
            self.print_red(
                " [!] Request ConnectionError: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except Exception as e:
            self.print_red(
                " [!] Request Unknown Error: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False

    def request_content(self, url, return_code=200):
        """
        Request content and expected return code.
        :param url:  URL to request
        :param return_code: expected return code or raise error
        :return: JSON, SuccessState
        """
        try:
            header = {
                'User-Agent': str(self.ua.google)
            }
            if not validators.url(url):
                self.print_yellow(
                    " [!] Invalid URL Requested: %s" % (str(url)))
                return {}, False
            r = requests.get(url, headers=header)
            if r.status_code != return_code:
                self.print_yellow(" [!] Request returned invalid status code: (CODE): %s (EXPECTED): %s" %
                                  (str(r.status_code), str(return_code)))
                return {}, False
            return r.content, True
        except requests.ConnectTimeout as e:
            self.print_red(
                " [!] Request ConnectionTimeout: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.TooManyRedirects as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.HTTPError as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except ConnectionError as e:
            self.print_red(
                " [!] Request ConnectionError: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except Exception as e:
            self.print_red(
                " [!] Request Unknown Error: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False

    def request_text(self, url, return_code=200):
        """
        Request content and expected return code.
        :param url:  URL to request
        :param return_code: expected return code or raise error
        :return: JSON, SuccessState
        """
        try:
            header = {
                'User-Agent': str(self.ua.google)
            }
            if not validators.url(url):
                self.print_yellow(
                    " [!] Invalid URL Requested: %s" % (str(url)))
                return {}, False
            r = requests.get(url, headers=header)
            if r.status_code != return_code:
                self.print_yellow(" [!] Request returned invalid status code: (CODE): %s (EXPECTED): %s" %
                                  (str(r.status_code), str(return_code)))
                return {}, False
            return r.text, True
        except requests.ConnectTimeout as e:
            self.print_red(
                " [!] Request ConnectionTimeout: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.TooManyRedirects as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.HTTPError as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except ConnectionError as e:
            self.print_red(
                " [!] Request ConnectionError: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except Exception as e:
            self.print_red(
                " [!] Request Unknown Error: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False

    def request_raw(self, url, return_code=200):
        """
        Request content and expected return code.
        :param url:  URL to request
        :param return_code: expected return code or raise error
        :return: JSON, SuccessState
        """
        try:
            header = {
                'User-Agent': str(self.ua.google)
            }
            if not validators.url(url):
                self.print_yellow(
                    " [!] Invalid URL Requested: %s" % (str(url)))
                return {}, False
            r = requests.get(url, headers=header)
            if r.status_code != return_code:
                self.print_yellow(" [!] Request returned invalid status code: (CODE): %s (EXPECTED): %s" %
                                  (str(r.status_code), str(return_code)))
                return {}, False
            return r, True
        except requests.ConnectTimeout as e:
            self.print_red(
                " [!] Request ConnectionTimeout: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.TooManyRedirects as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except requests.HTTPError as e:
            self.print_red(
                " [!] Request TooManyRedirects: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except ConnectionError as e:
            self.print_red(
                " [!] Request ConnectionError: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
        except Exception as e:
            self.print_red(
                " [!] Request Unknown Error: (URL): %s (ERROR): %s" % (str(url), str(e)))
            return {}, False
