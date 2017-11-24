from termcolor import colored, cprint
import json

class CorePrinters(object):
    """
    Core class: handles all data output within the project.
    """

    __title_screen = """
    ------------------------------------------------------------
      ______  _______                                 __          
     /      \/       \                               /  |         
    /$$$$$$  $$$$$$$  | ______  _____  ____   ______ $$/ _______  
    $$ \__$$/$$ |  $$ |/      \/     \/    \ /      \/  /       \ 
    $$      \$$ |  $$ /$$$$$$  $$$$$$ $$$$  |$$$$$$  $$ $$$$$$$  |
     $$$$$$  $$ |  $$ $$ |  $$ $$ | $$ | $$ |/    $$ $$ $$ |  $$ |
    /  \__$$ $$ |__$$ $$ \__$$ $$ | $$ | $$ /$$$$$$$ $$ $$ |  $$ |
    $$    $$/$$    $$/$$    $$/$$ | $$ | $$ $$    $$ $$ $$ |  $$ |
     $$$$$$/ $$$$$$$/  $$$$$$/ $$/  $$/  $$/ $$$$$$$/$$/$$/   $$/ 
    ------------------------------------------------------------                                                                                              
    """

    def __init__(self):
        """
        INIT class object and define
        statics.
        """
        self.print_green = lambda x: cprint(x, 'green')
        self.print_green_on_bold = lambda x: cprint(x, 'green', attrs=['bold'])
        self.print_yellow = lambda x: cprint(x, 'yellow')
        self.print_yellow_on_bold = lambda x: cprint(x, 'yellow', attrs=['bold'])
        self.print_red = lambda x: cprint(x, 'red')
        self.print_red_on_bold = lambda x: cprint(x, 'red', attrs=['bold'])
        self.print_white = lambda x: cprint(x, 'white')

    def print_entry(self):
        """
        Print entry screen to the project.
        :return: NONE
        """
        self.print_green_on_bold(self.__title_screen)

    def print_modules(self, module_list):
        """
        Print all modules within the framework to be run
        :param module_list: mod list of loaded functions 
        :return: NONE
        """
        self.print_red_on_bold(" [*] Available modules are:")
        x = 1
        ordlist = []
        finalList = []
        for name in module_list:
            parts = name.split("/")
            ordlist.append(parts[-1])
        ordlist = sorted(ordlist)
        for name in ordlist:
            name = 'modules/' + name
            finalList.append(name)
        for name in finalList:
            print("\t%s)\t%s" % (x, '{0: <24}'.format(name)))
            x += 1

    def print_modules_long(self, module_list):
        """
        Print all modules within the framework to be run
        :param module_list: mod list of loaded functions 
        :return: NONE
        """
        self.print_red_on_bold(" [*] Available modules are:")
        print("-" * 60)
        for mod in module_list:
            dynamic_module = module_list[mod]
            dm = dynamic_module.DynamicModule()
            parts = mod.split("/")
            name = 'modules/' + parts[-1]
            self.print_yellow_on_bold(" %s" % ('{0: <24}'.format(name).ljust(40)))
            print(json.dumps(dm.info, indent=4))
            print("-" * 60)


    def formatLong(self, title, message, frontTab=True, spacing=16):
        """
        Print a long title:message with our standardized formatting.
        Wraps multiple lines into a nice paragraph format.
        """

        lines = textwrap.wrap(textwrap.dedent(message).strip(), width=50)
        returnstring = ""

        i = 1
        if len(lines) > 0:
            if frontTab:
                returnstring += "\t%s%s" % (('{0: <%s}' %
                                             spacing).format(title), lines[0])
            else:
                returnstring += " %s%s" % (('{0: <%s}' %
                                            (spacing-1)).format(title), lines[0])
        while i < len(lines):
            if frontTab:
                returnstring += "\n\t"+' '*spacing+lines[i]
            else:
                returnstring += "\n"+' '*spacing+lines[i]
            i += 1
        return returnstring