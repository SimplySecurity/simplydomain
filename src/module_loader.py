# Loads modules into the system

import glob
import warnings
import importlib


class LoadModules(object):
    """
    Loads modules from the "modules" directory allowing
    operators to drop modules into the folder.
    """
    def __init__(self):
        """
        Create objects used in class.
        """
        self.modules = {}
        self.dmodules = {}
        self.load_modules()

    def load_modules(self):
        """
        Loads modules into static class variables, 
        these can than be referenced easily.
        :return: NONE
        """
        # loop and assign key and name
        warnings.filterwarnings('ignore', '.*Parent module*', )
        x = 1
        for name in glob.glob('modules/*.py'):
            if name.endswith(".py") and ("__init__" not in name) \
                    and ("module_template" not in name):
                module_name = name.replace("/", ".").rstrip('.py')
                loaded_modules = self.dynamic_import(module_name)
                self.modules[name] = loaded_modules
                self.dmodules[x] = loaded_modules
                x += 1

    def dynamic_import(self, module):
        """
        Loads a module at runtime.
        :param module: module str (name)
        :return: module obj
        """
        return importlib.import_module(module)