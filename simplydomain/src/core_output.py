import json
import os
import pathlib
import time

from . import core_printer


class CoreOutput(core_printer.CorePrinters):
    """
    Core class to handle final output.
    """

    def __init__(self):
        """
        Init class.
        """
        core_printer.CorePrinters.__init__(self)
        self.json_data = {}

    def output_json_obj(self, json_data):
        """
        Output json data file.
        :param json_data: json obj
        :return: NONE
        """
        return json.dumps(json_data.subdomains, sort_keys=True)

    def output_json(self, json_data):
        """
        Output json data file.
        :param json_data: json obj
        :return: NONE
        """
        args = self.config['args']
        s = str(args.DOMAIN)
        s = s.replace('.', '-')
        loc = ""
        dir_name = s + '-' + str(int(time.time()))
        def_name = s + '.json'
        if args.output:
            loc += str(args.output)
        if args.output_name:
            dir_name = str(args.output_name)
        dir_to_write = os.path.join(loc, dir_name)
        pathlib.Path(dir_to_write).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(dir_to_write, def_name), 'a') as outfile:
            json.dump(json_data.subdomains, outfile, sort_keys=True, indent=4)
        self.logger.infomsg('output_json() JSON output file created at: : '
                            + str((os.path.join(dir_to_write, def_name))), 'CoreOutput')
        print(self.blue_text("JSON text file created: %s" %
                             (os.path.join(dir_to_write, def_name))))

    def print_text(self, json_data):
        """
        Output to text file
        :param json_data: json obj
        :return: NONE
        """
        for item in json_data.subdomains['data']:
            print("name:%s module_name:%s module_version:%s source:%s time:%s toolname:%s subdomain:%s vaild:%s" %
                  (item['name'], item['module_name'], item['module_version'], item['source'], item['time'],
                   item['toolname'], item['subdomain'], item['valid']))

    def output_text(self, json_data):
        """
        Output to text file
        :param json_data: json obj
        :return: NONE
        """
        args = self.config['args']
        s = str(args.DOMAIN)
        s = s.replace('.', '-')
        loc = ""
        dir_name = s + '-' + str(int(time.time()))
        def_name = s + '.grep'
        if args.output:
            loc += str(args.output)
        if args.output_name:
            dir_name = str(args.output_name)
        dir_to_write = os.path.join(loc, dir_name)
        pathlib.Path(dir_to_write).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(dir_to_write, def_name), 'a') as outfile:
            for item in json_data.subdomains['data']:
                x = ("name:%s module_name:%s module_version:%s source:%s time:%s toolname:%s subdomain:%s vaild:%s\n" %
                     (item['name'], item['module_name'], item['module_version'], item['source'], item['time'],
                      item['toolname'], item['subdomain'], item['valid']))
                outfile.write(x)
        self.logger.infomsg('output_text() TXT grep output file created at: : '
                            + str(os.path.join(dir_to_write, def_name)), 'CoreOutput')
        print(self.blue_text("Grepable text file created: %s" %
                             (os.path.join(dir_to_write, def_name))))

    def output_text_std(self, json_data):
        """
        Output to text file
        :param json_data: json obj
        :return: NONE
        """
        args = self.config['args']
        s = str(args.DOMAIN)
        s = s.replace('.', '-')
        loc = ""
        dir_name = s + '-' + str(int(time.time()))
        def_name = s + '.txt'
        if args.output:
            loc += str(args.output)
        if args.output_name:
            dir_name = str(args.output_name)
        dir_to_write = os.path.join(loc, dir_name)
        pathlib.Path(dir_to_write).mkdir(parents=True, exist_ok=True)
        flist = []
        with open(os.path.join(dir_to_write, def_name), 'a') as outfile:
            for item in json_data.subdomains['data']:
                flist.append(item['subdomain'])
            for item in sorted(set(flist)):
                x = ("%s\n" % (item))
                outfile.write(x)
        self.logger.infomsg('output_text_std() TXT output file created at: : '
                            + str((os.path.join(dir_to_write, def_name))), 'CoreOutput')
        print(self.blue_text("Standard text file created: %s" %
                             (os.path.join(dir_to_write, def_name))))
