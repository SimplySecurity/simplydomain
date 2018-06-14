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
            # name of the module to be used
            'Name': 'Template enumerator module',

            # version of the module to be used
            'Version': '0.0',

            # description
            'Description': ('Template module to model after',
                            'while using 2 lines'),

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI', '@Killswitch-GUI'],

            # list of resources or comments
            'comments': [
                'Please make sure all of the required fields are filled in.',
                'Http://www.google.com'
            ]
        }

        self.options = {
            # options for the module to use by default these will be dynamic in nature

            # threads for the module to use
            'Threads': 10

        }

    def dynamic_main(self, queue_dict):
        """
        Main entry point for process to call.
        :return: 
        """
