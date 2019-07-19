#!/usr/bin/env python3
#cat-like program
import sys
import re
import os


class Argparse:
    available_options = ['-n', '-h', '-e', '-t']

    def __init__(self, arg_list):
        self.options = []
        self.filenames = []
        self.invalid_options = []
        self.line_numbers = False
        self.eol_indicator = False
        self.tab_character = False
        self.read_stdin = False

        option = re.compile('^-.*')
        for i in arg_list[1:]:
            if option.match(i):
                self.options.append(i)
            else:
                self.filenames.append(i)
        for i in self.options:
            if i not in self.available_options:
                self.invalid_options.append(i)
        if  self.invalid_options:
            print("invalid option: ")
            for i in self.invalid_options:
                print(i)
            print('try cat.py -h for more information')
            sys.exit()
        if '-h' in self.options:
                print(
"""cat-like program to display content of files.Reads from stdin if no file given.
Available options:
-n  display line numbers
-e  put $ at the end of each line
-t  replace TAB characters with ^I
-h  display this help text"""
)
                sys.exit()
        if "-n" in self.options:
            self.line_numbers = True
        if "-e" in self.options:
            self.eol_indicator = True
        if "-t" in self.options:
            self.tab_character = True
        if  not self.filenames:
            self.read_stdin = True


def cat(arg):
    if not arg.read_stdin:
        for k in arg.filenames:
            try:
                f = open(k, "rt")
            except FileNotFoundError:
                print('Error, No such file as: "', i, '"') 
                sys.exit(1)
            do_cat(f, arg)
            f.close()
    else:
        while True:
            try:
                text = []
                if not os.isatty(0):
                    for line in sys.stdin:
                        text.append(line)
                else:
                    text.append(input())
                do_cat(text, arg)
                if len(text) != 1:
                    sys.exit(0)
                print('')
            except KeyboardInterrupt:
                print('')
                sys.exit(1)

def do_cat(file, arg):
    if not arg.read_stdin:
        content = file.readlines()
    else:
        content = file
    for i, j in enumerate(content):
        if arg.tab_character == False:
            line = j
        if arg.tab_character:
            line = ""
            for l in j:
                if l == "\t":
                    line += "^I"
                else:
                    line += l
        if arg.line_numbers:
            sys.stdout.write(str(i+1))
            sys.stdout.write(' ')
        if arg.eol_indicator == False:
            sys.stdout.write(line)
        if arg.eol_indicator:
            line_eol = ''
            for k in line:
                if k != '\n':
                    line_eol += k
            if os.isatty(0):
                line_eol += '$'
            else:
                line_eol += '$\n'
            sys.stdout.write(line_eol)


def main():
        #print(sys.argv)
        arg = Argparse(sys.argv)
        cat(arg)


main()
