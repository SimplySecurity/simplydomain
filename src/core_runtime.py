import time
import signal
import sys
from . import module_loader
from . import core_processes


class CoreRuntime(module_loader.LoadModules,
                  core_processes.CoreProcess):
    """
    Core Runtime Class.
    """

    def __init__(self, logger):
        """
        Init class and passed objects.
        """
        module_loader.LoadModules.__init__(self)
        # core_printer.CorePrinters.__init__(self)
        core_processes.CoreProcess.__init__(self)
        self.logger = logger

    def list_modules(self):
        """
        List the modules loaded.
        :return: 
        """
        self.logger.debugmsg('tasked to list modules', 'CoreRuntime')
        self.print_modules(self.modules)

    def execute_mp(self):
        """
        Executes all the Dynamic Modules to be 
        sent to processes
        :return: 
        """
        self.populate_task_queue(self.modules)
        self.start_processes()
        while self.check_active():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.print_red_on_bold("\n[!] CRITICAL: CTRL+C Captured - Trying to clean up!\n"
                                       "[!] WARNING: Press CTRL+C AGAIN to bypass and MANUALLY cleanup")
                try:
                    time.sleep(1)
                    self.kill_processes()
                    sys.exit(0)
                except KeyboardInterrupt:
                    self.list_processes()
                    sys.exit(0)
        self.join_processes()







