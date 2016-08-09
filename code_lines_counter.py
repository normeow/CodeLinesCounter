# -*- coding: utf-8 -*-

import sys
import os
import re

class LinesCounter:
    extensions = [".cpp", ".java", ".py", ".cs"]
    def __init__(self):


        self.ignorstr = {
            ".cpp" : "^(//|using|#include)",
            ".java" : "^(package|import|//)",
            ".py" : "^{#|import|\n}",
            ".cs" : "^//|^using (\w+|(\w*\.)+\w+)$|^///"
        }

        self.ignorfilename = {
            ".cs" : "{\.Designer.cs}"
        }

        self.ignore_multilines = {
            ".cs" : ["/*", "*/"],
            ".cpp" : ["/*", "*/"],
            ".java": ["/*", "*/"],
            ".py": ["'''", "'''"]

        }

        self.res = {}
        self.file_pattern = "\.(\w*)"

    def get_lines_count(self, dir, extns):
        if extns == None:
            extns = self.extensions
        self.res = dict.fromkeys(extns, 0)
        self.countlines(dir,extns)
        return self.res

    def count_lines_in_file(self, file, ex):
        if ex in self.ignorfilename.keys():
            if re.search(self.ignorfilename[ex], file) != None:
                return

        f = open(file)
        mltlcomment = False;
        if ex in self.ignore_multilines:
            openmlt = self.ignore_multilines[ex][0]
            closemlt = self.ignore_multilines[ex][1]

        if ex in self.ignorstr.keys():
            ignore_pattern = self.ignorstr[ex]
        for line in f:
            if not mltlcomment:
                if openmlt in line:
                    mltlcomment == True
                elif re.search(ignore_pattern, line) == None:
                    self.res[ex] += 1
            else:
                if closemlt in line:
                    mltlcomment = False

    def countlines(self, dir, extns):
        ls = os.listdir(dir)
        for it in ls:
            path = dir + "/" + it
            if os.path.isdir(path):
                self.countlines(path, extns)
                continue
            ex = re.search(self.file_pattern, it)
            if ex != None:
                if ex.group(0) in extns:
                    self.count_lines_in_file(path, ex.group(0))

#TODO argparser
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error, no arguments")
        print("[-path] [-extensions] {optional}")
        exit(1)

    dir = sys.argv[1]
    if len(sys.argv) == 2:
        extensions = None
    else:
        extensions = sys.argv[2:]
    counter = LinesCounter()
    print(counter.get_lines_count(dir, extensions))
