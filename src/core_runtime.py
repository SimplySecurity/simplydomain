import sys
import time

from . import core_output
from . import core_processes
from . import module_loader


class CoreRuntime(module_loader.LoadModules,
                  core_processes.CoreProcess,
                  core_output.CoreOutput):
    """
    Core Runtime Class.
    """

    def __init__(self, logger, config):
        """
        Init class and passed objects.
        """
        self.config = config
        core_output.CoreOutput.__init__(self)
        module_loader.LoadModules.__init__(self)
        # ore_printer.CorePrinters.__init__(self)
        core_processes.CoreProcess.__init__(self)
        self.logger = logger


    def list_modules(self):
        """
        List the modules loaded.
        :return: 
        """
        self.logger.debugmsg('tasked to list modules', 'CoreRuntime')
        self.print_modules(self.modules)

    def list_modules_long(self):
        """
        List the modules loaded.
        :return: 
        """
        self.logger.debugmsg('tasked to list modules', 'CoreRuntime')
        self.print_modules_long(self.modules)

    def execute_output(self):
        """
        Execute the output of formatted data stucs.
        :return: NONE
        """
        self.output_text(self.serialize_json_output)
        self.output_json(self.serialize_json_output)
        self.output_text_std(self.serialize_json_output)


    def execute_startup(self):
        """
        setup Q.
        :return: NONE
        """
        self.print_d_module_start()
        self.populate_task_queue(self.modules)
        self.start_processes()


    def execute_dynamic(self):
        """
        Execute only the dynamic modules.
        :return: NONE
        """
        self._start_thread_function(self._pbar_thread)
        while self.check_active():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.print_red_on_bold("\n[!] CRITICAL: CTRL+C Captured - Trying to clean up!\n"
                                       "[!] WARNING: Press CTRL+C AGAIN to bypass and MANUALLY cleanup")
                try:
                    time.sleep(0.1)
                    self.stop_threads()
                    self.kill_processes()
                    sys.exit(0)
                except KeyboardInterrupt:
                    self.list_processes()
                    sys.exit(0)
        # cleanup dynamic mod pbar
        self.progress_bar_pickup.put(None)
        self.close_progress_bar()

    def execute_static(self):
        """
        Execute static modules in sorted order by EXEC order.
        :return: NONE
        """
        self.print_s_module_start()
        queue_dict = {
            'task_queue': self.task_queue,
            'task_output_queue': self.task_output_queue
        }
        if self.config['args'].wordlist_bruteforce:
            self.execute_process('src/static_modules/subdomain_bruteforce.py', self.config, queue_dict)

    def execute_mp(self):
        """
        Executes all the Dynamic Modules to be 
        sent to processes
        :return: 
        """
        try:
            # startup
            self.execute_startup()
            self.execute_dynamic()
            self.execute_static()
        finally:
            # cleanup
            self.join_processes()
            self.join_threads()
            self.execute_output()








