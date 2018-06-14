from validators import domain


class Scrub(object):

    """
    Core data handler to clean, and post results in proper
    DataSerialization format for SimplyDomain.

    Attributes:
        subdomain: subdomain to parse
    """

    def __init__(self, subdomain=""):
        """
        Init class struc. Used as a object to parse and populate
        results.
        """
        self.subdomain = subdomain

    def validate_domain(self):
        """
        Use domain validator to confirm domain name. 
        :return: BOOL
        """
        try:
            val = domain(str(self.subdomain))
            if val:
                # domain is valid
                return True
            else:
                # domain validation failed
                return False
        except Exception as e:
            # TODO: add in logger class for errors
            return False
