import multiprocessing as mp
from . import core_printer

class CoreProcess(core_printer.CorePrinters):
    """
    Core class to handle threading and process 
    creation.
    """

    def __init__(self):
        """
        Init class.

        Process creation steps:
        1) populate_task_queue() - with modules
        2) 
        """
        core_printer.CorePrinters.__init__(self)
        self.procs = []
        self.processors = mp.cpu_count()
        self.mp = mp
        self.mpq = self.mp.Queue()
        self.task_queue = mp.Queue()
        self.task_output_queue = mp.Queue()

    def _configure_mp(self):
        """
        Sets the configuration props for 
        mp to handle taskings.
        :return: NONE
        """
        # use SPAWN since FORK is not supported on windows
        # SPAWN is slower since it creates a entire python
        # interpter
        self.mp.set_start_method('spawn')

    def _configure_processes(self, mod_count):
        """
        Check to make sure we dont start
        more procs than needed. Also fill taskQ with
        None values (PILLS)
        :return: NONE
        """
        if self.processors > mod_count:
            self.processors = mod_count
        # populate the PILL == None
        for p in range(self.processors):
            self.task_queue.put(None)

    def populate_task_queue(self, modules):
        """
        Populats the queue of module objects to be executed.
        :param modules: passed list of dynamic loaded modules
        :return: NONE
        """
        for mod in modules:
            # populate the q with module data
            self.task_queue.put(mod)
        self._configure_processes(len(modules))

    def clear_task_queue(self):
        """
        If tasked to shutdown, clear the queue for cleanup
        :return: NONE
        """
        # empty the pipe q
        while not self.task_queue.empty():
            obj = self.task_queue.get()
            del obj
        # allow GC to pick up and flush pipe
        self.task_queue.close()

    def start_processes(self):
        """
        Executes all procs with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param module_obj: Module Ooject
        :param queues: A list of queue objects
        :return: BOOL 
        """
        queues = []
        for _ in range(self.processors):
            self.start_process(self.config, self.task_queue, self.task_output_queue)
        for p in self.procs:
            p.daemon = True
            p.start()

    def start_process(self, config, task_queue, task_output_queue):
        """
        Executes a proc with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param module_obj: Module Ooject
        :param queues: A list of queue objects
        :return: BOOL 
        """
        # add all process to a list so we itt over them
        queue_dict = {
            'task_queue': task_queue,
            'task_output_queue': task_output_queue
        }
        self.procs.append(
            self.mp.Process(target=self.execute_processes,
                            args=(config,queue_dict)))

    def execute_processes(self, config, queue_dict):
        """
        Executes the module required and passed.
        :param module_obj: module settings
        :param queues: passed list obj
        :return: 
        """
        while True:
            # loop to execute taskings from taskQ
            q = queue_dict['task_queue'].get()
            dynamic_module = self.modules[q]
            try:
                dm = dynamic_module.DynamicModule(config)
                self.print_green(" [*] Executing module: %s %s" %('{0: <22}'.format("("+dm.info['Module']+")"), "("+dm.info['Name']+")"))
                dm.dynamic_main(queue_dict)
            except Exception as e:
                print(e)
            break
        return 0

    def check_active(self):
        """
        Check if mp is has active pids
        :return: BOOL
        """
        if len(self.mp.active_children()):
            return True
        else:
            return False

    def join_processes(self):
        """
        Attempt to join all the process to clean 
        them up.
        :return: NONE
        """
        for p in self.procs:
            p.join()

    def list_processes(self):
        """
        List all procs and pids.
        :return: NONE
        """
        for p in self.procs:
            pid = p.pid
            p_name = p.name
            self.print_yellow("[!] Process info: (PID: %s) (NAME: %s)" % (str(pid), str(p_name)))

    def list_processes_exitcode(self):
        """
        List all procs and exitcode
        :return: 
        """
        for p in self.procs:
            pid = p.pid
            ec = p.exitcode
            self.print_yellow("[!] Process info: (PID: %s) (EXITCODE: %s)" % (str(pid), str(ec)))

    def kill_processes(self):
        """
        Attempt to kill all child pids
        and clean up from CTRL+C.
        :return: NONE
        """
        for p in self.procs:
            pid = p.pid
            p_name = p.name
            while p.is_alive():
                p.terminate()
            self.print_red("[!] Process has been terminated: (PID: %s) (NAME: %s" % (str(pid), str(p_name)))

