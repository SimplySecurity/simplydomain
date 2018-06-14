from tqdm import tqdm


class CoreProgress(object):

    """
    Core class for dynamic modules and progress bars.
    Also allows to use core printers with tqdm.write()
    """

    def __init__(self):
        """
        INIT class object and define
        statics.
        """
        # self.progress_bar
        pass

    def update_progress_bar(self):
        """
        Adds a completion record to the progress bar.
        :return:
        """
        self.progress_bar.update()

    def close_progress_bar(self):
        """
        Progress bar cleanup
        :return: NONE
        """
        self.progress_bar.close()

    def progress_print(self, msg_obj):
        """
        Prints a message obj to te tqdm loop.
        :param msg_obj: A obj to be be printed
        :return: NONE
        """
        self.progress_bar.write(msg_obj)

    def start_progress_bar(self, count, maxinterval=1, mininterval=0):
        """
        Start up pbar and show on screen.
        :param count: count of modules
        :return: NONE
        """
        self.progress_bar = tqdm(
            total=count, unit="module", maxinterval=maxinterval, mininterval=mininterval)

    def inc_progress_bar(self, size=0):
        """
        Incs the progrss by (1)
        :param size: If size pass size, otherwise do min inc.
        :return: NONE
        """
        if size:
            self.progress_bar.update(size)
        else:
            self.progress_bar.update()
