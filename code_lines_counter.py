# -*- coding: utf-8 -*-

import sys
import os
import re

class LinesCounter:
    extensions = [".cpp", ".java", ".py", ".cs"]
    def __init__(self):
        self._ignorstr = {
            ".cpp" : "^(//|using|#include)",
            ".java" : "^(package|import|//)",
            ".py" : "^{#|import|\n}",
            ".cs" : "^//|^using (\w+|(\w*\.)+\w+)$|^///"
        }

        self._ignorfilename = {
            ".cs" : "{\.Designer.cs}"
        }

        self._ignore_multilines = {
            ".cs" : ["/*", "*/"],
            ".cpp" : ["/*", "*/"],
            ".java": ["/*", "*/"],
            ".py": ["'''", "'''"]

        }

        self._res = {}
        self._file_pattern = "\.(\w*)"

    def get_lines_count(self, dir, extns):
        if extns == None:
            extns = self.extensions
        self._res = dict.fromkeys(extns, 0)
        self._countlines(dir, extns)
        return self._res

    def _count_lines_in_file(self, file, ex):
        if ex in self._ignorfilename.keys():
            if re.search(self._ignorfilename[ex], file) != None:
                return

        f = open(file)
        nopattern = True
        if ex in self._ignorstr.keys():
            ignore_pattern = self._ignorstr[ex]
            nopattern = False

        canbemulticomment = False
        mltlcomment = False;
        if ex in self._ignore_multilines:
            openmlt = self._ignore_multilines[ex][0]
            closemlt = self._ignore_multilines[ex][1]
            canbemulticomment = True

        if canbemulticomment:
            for line in f:
                line = line.strip()
                if not mltlcomment:
                    if openmlt in line:
                        if closemlt not in line:
                          mltlcomment == True
                        if line.find(openmlt) != 0:
                            self._res[ex] += 1
                    else:
                        if nopattern or self._islineok(ignore_pattern, line):
                            self._res[ex] += 1
                else:
                    if closemlt in line:
                        mltlcomment = False
                        if line.find(closemlt) != len(line) - len(closemlt):
                            self._res[ex] += 1
                    self._res[ex] += 1
        else:
            for line in f:
                if nopattern or self._islineok(ignore_pattern, line):
                    self._res[ex] += 1


    def _islineok(self, ignore_pattern, line):
        return re.search(ignore_pattern, line) == None

    def _countlines(self, dir, extns):
        if not os.path.exists(dir):
            raise Exception("Directory " + dir + " doesn't exist" );
        ls = os.listdir(dir)
        for it in ls:
            path = dir + "/" + it
            if os.path.isdir(path):
                self._countlines(path, extns)
                continue
            ex = re.search(self._file_pattern, it)
            if ex != None:
                if ex.group(0) in extns:
                    self._count_lines_in_file(path, ex.group(0))


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
    try:
        print(counter.get_lines_count(dir, extensions))
    except Exception as ex:
        print(repr(ex))
