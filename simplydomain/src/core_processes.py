import multiprocessing as mp
from itertools import product
import string
import threading
import time

from . import core_printer
from . import core_progress
from . import core_serialization
from . import module_recursion


class CoreProcess(core_printer.CorePrinters, core_progress.CoreProgress, module_recursion.ModuleRecursion):
    """
    Core class to handle threading and process 
    creation.
    """

    def __init__(self):
        """class init
        
        setups for a full MP stack.
        """
        core_printer.CorePrinters.__init__(self)
        core_progress.CoreProgress.__init__(self)
        module_recursion.ModuleRecursion.__init__(self)
        self.procs = []
        self.threads = []
        self.processors = mp.cpu_count()
        self.module_count = 0
        self.mp = mp
        self.mpq = self.mp.Queue()
        self.task_queue = mp.Queue()
        self.task_output_queue = mp.Queue()
        self.task_msg_queue = mp.Queue()
        self.progress_bar_pickup = mp.Queue()

        # output handlers
        self.serialize_json_output = core_serialization.SerializeJSON(
            self.config)

    def _configure_mp(self):
        """
        Sets the configuration props for 
        mp to handle taskings.
        :return: NONE
        """
        # use SPAWN since FORK is not supported on windows
        # SPAWN is slower since it creates a entire python
        # interpter

        self.logger.infomsg(
            'setting MP to SPAWN for cross platform support', 'CoreRuntime')
        self.mp.set_start_method('spawn')

    def _configure_processes(self, mod_count):
        """
        Check to make sure we dont start
        more procs than needed. Also fill taskQ with
        None values (PILLS)
        :return: NONE
        """
        self.logger.infomsg('current # of modules loaded: ' +
                            str(mod_count), 'CoreProcess')
        self.logger.infomsg('current # of processors of SYSTEM: ' +
                            str(self.processors), 'CoreProcess')
        if self.processors > mod_count:
            self.logger.infomsg('setting MP count of: ' +
                                str(mod_count), 'CoreProcess')
            self.processors = mod_count
        # populate the PILL == None
        for p in range(self.processors + 1):
            self.task_queue.put(None)

    def _task_output_queue_consumer(self):
        """
        Consumes task_output_queue data at set interval,
        to be run as a Thread at a interval of 1 sec. If this res
        is to low queue mem could lock.
        :return: NONE
        """
        while True:
            item = self.task_output_queue.get()
            if item:
                self.logger.debugmsg('_task_output_queue_consumer recv a subdomain: '
                                     + str(item.subdomain), 'CoreProcess')
                msg = self.green_text("Subdomain: %s Vaild: (%s)" %
                                      ('{0: <30}'.format('('+str(item.subdomain)+')'), str(item.valid)))
                if not self.config['silent']:
                    self.progress_print(msg)
                self.serialize_json_output.add_subdomain(item)
                self.add_subdomain(item)
            if item == None:
                self.logger.infomsg(
                    '_task_output_queue_consumer is (NONE) exiting thread', 'CoreProcess')
                break
            if self.task_output_queue.empty():
                pass
                # time.sleep(0.1)

    def populate_task_queue(self, modules):
        """
        Populats the queue of module objects to be executed.
        :param modules: passed list of dynamic loaded modules
        :param module_name: if name passed it will only place that module into the q
        :return: NONE
        """
        if self.config['args'].module:
            # populate only one module in the q
            for mod in modules:
                # populate the q with module data if name hits
                if self.config['args'].module in mod:
                    self.task_queue.put(mod)
        else:
            for mod in modules:
                # populate the q with module data
                self.logger.infomsg('adding module to task queue: ' +
                                    str(mod), 'CoreProcess')
                self.task_queue.put(mod)
        self.module_count = len(modules)
        self._configure_processes(len(modules))

    def clear_task_queue(self):
        """
        If tasked to shutdown, clear the queue for cleanup
        :return: NONE
        """
        # empty the pipe q
        self.logger.infomsg('tasked to clear_task_queue()', 'CoreProcess')
        while not self.task_queue.empty():
            obj = self.task_queue.get()
            del obj
        # allow GC to pick up and flush pipe
        self.logger.infomsg(
            'clear_task_queue() completed empty', 'CoreProcess')
        self.task_queue.close()

    def _pbar_thread(self):
        """
        Built be called from a thread and do simple
        math to watch progress of Dynamic modules.
        :return: NONE
        """
        if not self.config['silent']:
            start_count = len(self.procs)
            self.start_progress_bar(self.module_count)
            while self.check_active():
                try:
                    dm = self.progress_bar_pickup.get()
                except Exception as e:
                    print(e)
                if dm == None:
                    self.close_progress_bar()
                    break
                if dm:
                    if dm[0] == 'complete':
                        self.progress_print(self.blue_text(dm[1]))
                        self.inc_progress_bar(1)
                    if dm[0] == 'execute':
                        self.progress_print(self.blue_text(dm[1]))
                if self.progress_bar_pickup.empty():
                    time.sleep(0.1)

    def _start_thread_function(self, pointer):
        """
        starts a late or early thread.
        :param pointer: Function def
        :return: NONE
        """
        # TODO: FIX this hack and use real pointer?
        self.threads.insert(0, threading.Thread(
            target=self._pbar_thread()))

        t = self.threads[0]
        t.start()

    def _start_threads(self):
        """
        Function to handle threads to be spawned.
        :return: NONE
        """
        self.threads.append(threading.Thread(
            target=self._task_output_queue_consumer))

        for t in self.threads:
            # TODO: Fix issue where threads die before job is parsed
            # TODO: Make some threads daemon?
            # t.daemon = True
            t.start()

    def stop_threads(self):
        """
        Attempt to clean up threads before bail.
        :return: NONE
        """
        self.logger.infomsg(
            'tasked to stop_threads() putting (NONE)', 'CoreProcess')
        self.task_output_queue.put(None)
        for t in self.threads:
            self.logger.infomsg(
                'Attempting to shutting down thread in stop_threads()', 'CoreProcess')
            t.join
        self.print_red("[!] All consumer threads have been joined")
        self.logger.infomsg(
            'All consumer threads joined in stop_threads()', 'CoreProcess')

    def join_threads(self):
        """
        Attempt to clean up threads before bail.
        :return: NONE
        """
        self.logger.infomsg(
            'tasked to join_threads() putting (NONE)', 'CoreProcess')
        self.task_output_queue.put(None)
        while True:
            if self.task_output_queue.empty() == True:
                self.logger.infomsg(
                    'self.task_output_queue is empty! breaking loop', 'CoreProcess')
                break
            else:
                self.logger.infomsg(
                    'self.task_output_queue not empty sleeping for 1 second', 'CoreProcess')
                time.sleep(1)
        for t in self.threads:
            t.join

    def start_processes(self):
        """
        Executes all procs with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param module_obj: Module Ooject
        :param queues: A list of queue objects
        :return: BOOL 
        """
        self._start_threads()
        for _ in range(self.processors):
            self.logger.infomsg(
                'start_processes() is kicking off empty procs with queue objects', 'CoreProcess')
            self.start_process(self.config, self.task_queue,
                               self.task_output_queue, self.progress_bar_pickup)
        for p in self.procs:
            p.daemon = True
            p.start()
            self.logger.infomsg(
                'start_process() started proc with daemon mode', 'CoreProcess')

    def start_process(self, config, task_queue, task_output_queue, progress_bar_pickup):
        """
        Executes a proc with a given module and
        passes it the proper objects to communicate with
        the core run time.

        :param config: Module Ooject
        :param task_queue: A list of queue objects
        :param task_output_queue:
        :return: BOOL 
        """
        # add all process to a list so we itt over them
        queue_dict = {
            'task_queue': task_queue,
            'task_output_queue': task_output_queue,
            'progress_bar_pickup': progress_bar_pickup
        }
        self.logger.infomsg('start_process() built queue_dict and appending to self.mp.procs, current proc count: '
                            + str(len(self.procs)), 'CoreProcess')
        self.procs.append(
            self.mp.Process(target=self.execute_processes,
                            args=(config, queue_dict, self.modules)))

    def execute_processes(self, config, queue_dict, modules):
        """
        Executes the module required and passed.
        :param module_obj: module settings
        :param queues: passed list obj
        :return: 
        """
        while True:
            # loop to execute taskings from taskQ
            q = queue_dict['task_queue'].get()
            pbq = queue_dict['progress_bar_pickup']
            if q == None:
                self.logger.infomsg(
                    'execute_processes() dynamic module task_queue empty, EXITING process', 'CoreProcess')
                break
            dynamic_module = modules[q]
            try:
                dm = dynamic_module.DynamicModule(config)
                self.logger.infomsg('execute_processes() starting module: '
                                    + str(dm.info['Name']), 'CoreProcess')
                msg = "Executing module: %s %s" % ('{0: <22}'.format(
                    "("+dm.info['Module']+")"), "("+dm.info['Name']+")")
                if not self.config['silent']:
                    pbq.put(['execute', msg])
                # blocking
                dm.dynamic_main(queue_dict)
                self.logger.infomsg('execute_processes() completed module: '
                                    + str(dm.info['Name']), 'CoreProcess')
                msg = "Module completed: %s %s" % (
                    '{0: <22}'.format("(" + dm.info['Module'] + ")"), "(" + dm.info['Name'] + ")")
                if not self.config['silent']:
                    pbq.put(['complete', msg])
            except Exception as e:
                self.logger.warningmsg('execute_processes hit fatal error: '
                                       + str(e), 'CoreProcess')
                self.print_red(" [!] Module process failed: %s %s" % (
                    '{0: <22}'.format("(" + dm.info['Module'] + ")"), "(" + e + ")"))

    def execute_process(self, mod_name, config, queue_dict):
        """
        Executes the module required and passed.
        :param module_obj: module settings
        :param queues: passed list obj
        :return:
        """
        static_module = self.static_modules[mod_name]
        try:
            sm = static_module.DynamicModule(config)
            if not self.config['silent']:
                self.print_green(" [*] Executing module: %s %s" % (
                    '{0: <22}'.format("("+sm.info['Module']+")"), "("+sm.info['Name']+")"))
            sm.dynamic_main(queue_dict)
            if not self.config['silent']:
                self.print_green(" [*] Module completed: %s %s" % (
                    '{0: <22}'.format("(" + sm.info['Module'] + ")"), "(" + sm.info['Name'] + ")"))
        except Exception as e:
            if not self.config['silent']:
                self.print_red(" [!] Module process failed: %s %s" % (
                    '{0: <22}'.format("(" + sm.info['Module'] + ")"), "(" + str(e) + ")"))

    def check_active_len(self):
        """
        Checks for active pids and returns count.
        :return: int
        """
        _value = len(self.mp.active_children())
        self.logger.infomsg('check_active_len() checking current active pids: '
                            + str(_value), 'CoreProcess')
        return _value

    def check_active(self):
        """
        Check if mp is has active pids
        :return: BOOL
        """
        if len(self.mp.active_children()):
            self.logger.infomsg(
                'check_active() for MP pids: True', 'CoreProcess')
            return True
        else:
            self.logger.infomsg(
                'check_active() for MP pids: False', 'CoreProcess')
            return False

    def join_processes(self):
        """
        Attempt to join all the process to clean 
        them up.
        :return: NONE
        """
        for p in self.procs:
            self.logger.infomsg('join_processes() starting to join self.procs, current active: '
                                + str(len(self.procs)), 'CoreProcess')
            p.join()

    def list_processes(self):
        """
        List all procs and pids.
        :return: NONE
        """
        for p in self.procs:
            pid = p.pid
            p_name = p.name
            self.print_yellow(
                "[!] Process info: (PID: %s) (NAME: %s)" % (str(pid), str(p_name)))

    def list_processes_exitcode(self):
        """
        List all procs and exitcode
        :return: 
        """
        for p in self.procs:
            pid = p.pid
            ec = p.exitcode
            self.print_yellow(
                "[!] Process info: (PID: %s) (EXITCODE: %s)" % (str(pid), str(ec)))

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
            self.print_red("[!] Process has been terminated: (PID: %s) (NAME: %s)" % (
                str(pid), str(p_name)))
