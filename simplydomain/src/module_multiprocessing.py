import multiprocessing as mp


class ModuleMultiProcessing(object):

    """
    A multiprocessing class to handle execution for all modules
    requiring multiprocessing. Use module* before all items to we dont
    crush other mp classes.
    """

    def __init__(self):
        """
        Create objects used in class.
        """
        self.module_procs = []
        self.module_threads = []
        self.module_processors = mp.cpu_count()
        self.module_mp = mp

    def _module_configure_mp(self):
        """
        Sets the configuration props for
        mp to handle taskings.
        :return: NONE
        """
        # use SPAWN since FORK is not supported on windows
        # SPAWN is slower since it creates a entire python
        # interpter
        self.module_mp.set_start_method('spawn')

    def module_join_processes(self):
        """
        Attempt to join all the process to clean
        them up.
        :return: NONE
        """
        for p in self.module_procs:
            p.join()

    def modue_list_processes(self):
        """
        List all procs and pids.
        :return: NONE
        """
        for p in self.module_procs:
            pid = p.pid
            p_name = p.name
            print("[!] Process info: (PID: %s) (NAME: %s)" %
                  (str(pid), str(p_name)))

    def module_check_active(self):
        """
        Check if mp is has active pids
        :return: BOOL
        """
        if len(self.module_mp.active_children()):
            return True
        else:
            return

    def module_start_processes(self):
        """
        Executes all procs with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param module_obj: Module Ooject
        :param queues: A list of queue objects
        :return: BOOL
        """
        for _ in range(self.module_processors):
            self.module_start_process()
        for p in self.module_procs:
            p.daemon = True
            p.start()

    def module_start_process(self, function_pointer, queue_list):
        """
        Executes a proc with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param function_pointer: Module Object
        :return: BOOL
        """
        self.module_procs.append(
            self.module_mp.Process(target=function_pointer, args=(queue_list,)))
