#! /usr/bin/env python3

import argparse
import configparser
import os
import subprocess
import tempfile
from pathlib import Path

from yo import Colors, SubcommandHelpFormatter
        

class YoCommandHandler(object):
    def __init__(self, parser, filename='.yorc'):
        self.parser = parser
        self.filename = filename
        self.config = configparser.RawConfigParser(delimiters=('='))

    def _display_error(self, message, show_help=True, fatal=False):
        print(message, end='\n')
        if show_help:
            self.parser.print_help()
        if fatal:
            exit(0)

    def _get_config(self, args):
        filename = self.filename
        cwd = Path.cwd()
        rc_file = None
        if args.is_global:
            rc_file = Path("~/{}".format(filename))
        else:
            rc_file = Path(cwd, filename)
        rc_file = rc_file.expanduser()
        return rc_file

    def _read_config(self, args):
        rc_file = self._get_config(args)
        self.config.read(str(rc_file))

    def _write_config(self, args):
        rc_file = self._get_config(args)
        with rc_file.open(mode='w') as f:
            self.config.write(f)

    def init(self, args):
        """ Initialize yo configuration """
        rc_file = self._get_config(args)
        if not rc_file.is_file():
            with rc_file.open(mode='a') as f:
                f.write("# This is the command file\n\n")
        else:
            self._display_error("Yo, you already have a command file there. Check your usage:\n", show_help=True, fatal=True)
            return

    def destroy(self, args):
        """ Wipes yo configuration """
        rc_file = self._get_config(args)
        if rc_file.is_file():
            os.remove(str(rc_file))

    def add_command(self, args):
        """ Add a command """
        alias = args.alias
        command = ' '.join(args.command)
        self._read_config(args)
        if not self.config.has_section("commands"):
            self.config.add_section("commands")
        self.config.set("commands", alias, command)

        self._write_config(args)
        print("Yo, added command: {}={}".format(alias, command))

    def remove_command(self, args):
        """ Remove a command """
        alias = args.alias

        self._read_config(args)
        self.config.remove_option("commands", alias)
        self._write_config(args)

        print("Yo, removed command: {}".format(alias))

    def rename_command(self, args):
        """ Rename a command """
        alias1 = args.alias1
        alias2 = args.alias2

        self._read_config(args)
        command = self.config.get("commands", alias1)
        self.config.set("commands", alias2, command)
        self.config.remove_option("commands", alias1)
        self._write_config(args)

        print("Yo, renamed command {} to {}".format(alias1, alias2))

    def run_command(self, args):
        """ Run a command """
        alias = args.command
        self._read_config(args)
        command = self.config.get("commands", alias)

        if command:
            env = os.environ.copy()
            subprocess.Popen(command, shell=True, env=env).wait()

    def list_commands(self, args):
        """ List available commands """
        self._read_config(args)
        options = self.config.options("commands")

        longest = 0
        for option in options:
            length = len(option)
            if length > longest:
                longest = length
        print("\n{}Available commands\n".format(Colors.BOLD))
        for option in options:
            spaces = ' ' * (longest - len(option))
            print("{}{}{}{}{} = {}".format(spaces, Colors.BOLD, Colors.BLUE, option, Colors.NORM, self.config.get('commands', option)))
        print()
    
    def edit_config(self, args):
        """ Edit configuration in-place """
        editor = os.environ.get("EDITOR", "vi")
        config = self._get_config(args)
        conf_str = ""
        with config.open(mode="r") as c:
            conf_str = c.read()
        
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
            header = bytes("# Edit the contents below and save to update {}\n#\n{}".format(config, conf_str), encoding="utf-8")
            tmp.write(header)
            tmp.flush()
            tmp_modified = os.stat(tmp.name).st_mtime
            
            subprocess.call([editor, tmp.name])
            
            if os.stat(tmp.name).st_mtime > tmp_modified:
                tmp.seek(0)
                for index, line in enumerate(tmp):
                    if index <= 1 and line.decode()[0] == "#":
                        if line == b"#\n":
                            break
                    else:
                        exit("Temp file header is corrupt, aborting")
                
                edits = tmp.read()
                
                with config.open(mode="wb") as c:
                    c.write(edits)
            else:
                exit("No changes detected, cancelling edit")


YORC_FILE_NAME = ".yorc"
parser = argparse.ArgumentParser(description="Yo command runner", formatter_class=SubcommandHelpFormatter)
args = None

yo = YoCommandHandler(parser, YORC_FILE_NAME)


def cli():
    # Modifiers
    parser.add_argument("-g", "--global", dest="is_global", help="use global config", action="store_false")

    subparsers = parser.add_subparsers(title="commands")

    # Built-in commands
    parser_help = subparsers.add_parser("help", help="show this help message and exit")
    parser_help.set_defaults(func=lambda _: parser.print_help())

    parser_init = subparsers.add_parser("init", help="initialize command file")
    parser_init.set_defaults(func=yo.init)

    parser_destroy = subparsers.add_parser("destroy", aliases=['wipe'], help="remove command file")
    parser_destroy.set_defaults(func=yo.destroy)

    parser_add = subparsers.add_parser("add", help="add command")
    parser_add.add_argument('alias', help="the alias of the command")
    parser_add.add_argument('command', nargs="+", help="the command to run")
    parser_add.set_defaults(func=yo.add_command)

    parser_remove = subparsers.add_parser("remove", aliases=['rm'], help="remove command")
    parser_remove.add_argument('alias', help="the alias of the command")
    parser_remove.set_defaults(func=yo.remove_command)

    parser_rename = subparsers.add_parser("rename", aliases=['mv'], help="rename command")
    parser_rename.add_argument('alias1', help="the alias of the command")
    parser_rename.add_argument('alias2', help="the new alias of the command")
    parser_rename.set_defaults(func=yo.rename_command)

    parser_run = subparsers.add_parser("run", help="run command")
    parser_run.add_argument('command', help="the alias of the command")
    parser_run.set_defaults(func=yo.run_command)

    parser_list = subparsers.add_parser("list", aliases=['ls'], help="list available command")
    parser_list.set_defaults(func=yo.list_commands)
    
    parser_edit = subparsers.add_parser("edit", help="edit configuration")
    parser_edit.set_defaults(func=yo.edit_config)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(e)
        # parser.print_help()

if __name__ == "__main__":
    cli()
