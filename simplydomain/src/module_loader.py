# Loads modules into the system
import os
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
        self.static_modules = {}
        self.static_dmodules = {}
        self.load_dynamic_modules()
        self.load_static_modules()

    def load_dynamic_modules(self):
        """
        Loads modules into static class variables, 
        these can than be referenced easily.
        :return: NONE
        """
        # loop and assign key and name
        current_script_patch = os.path.dirname(os.path.abspath(__file__))
        warnings.filterwarnings('ignore', '.*Parent module*', )
        x = 1
        path = os.path.join('dynamic_modules', '*.py')
        path = current_script_patch + "/" + path
        for name in glob.glob(path):
            if name.endswith(".py") and ("__init__" not in name) \
                    and ("module_template" not in name):
                quick_path = os.path.join(
                    'simplydomain', 'src', 'dynamic_modules', name.split('/')[-1])
                module_name = quick_path.replace("/", ".").rstrip('.py')
                loaded_modules = self.dynamic_import(module_name)
                self.modules[quick_path] = loaded_modules
                self.dmodules[x] = loaded_modules
                x += 1

    def load_static_modules(self):
        """
        Loads modules into static class variables,
        these can than be referenced easily.
        :return: NONE
        """
        # loop and assign key and name
        current_script_patch = os.path.dirname(os.path.abspath(__file__))
        warnings.filterwarnings('ignore', '.*Parent module*', )
        x = 1
        path = os.path.join('static_modules', '*.py')
        path = current_script_patch + "/" + path
        for name in glob.glob(path):
            if name.endswith(".py") and ("__init__" not in name) \
                    and ("module_template" not in name):
                quick_path = os.path.join(
                    'simplydomain', 'src', 'static_modules', name.split('/')[-1])
                module_name = quick_path.replace("/", ".").rstrip('.py')
                loaded_modules = self.dynamic_import(module_name)
                self.static_modules[quick_path] = loaded_modules
                self.static_dmodules[x] = loaded_modules
                x += 1

    def dynamic_import(self, module):
        """
        Loads a module at runtime.
        :param module: module str (name)
        :return: module obj
        """
        return importlib.import_module(module)
