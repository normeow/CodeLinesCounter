import sys
import os
import re

class LinesCounter:
    def __init__(self):
        self.ignorstr = {
            ".cpp" : r"^{//|using|#include}",
            ".java" : r"^{package|import|//}",
            ".py" : r"^{#|import|\n}",
            ".cs" : r"^{//\w*|using\w*}$"
        }

        self.ignorfilename = {
            ".cs" : "{\.Designer.cs}"
        }

        self.res = {}
        self.file_pattern = "\.(\w*)"

    def get_lines_count(self, dir, extns):
        self.res = dict.fromkeys(extns, 0)
        self.countlines(dir,extns)
        return self.res

    def count_lines_in_file(self, file, ex):
        if ex in self.ignorfilename.keys():
            if re.search(self.ignorfilename[ex], file) != None:
                return

        f = open(file)
        ignore_pattern = ""
        if ex in self.ignorstr.keys():
            ignore_pattern = self.ignorstr[ex]
        mltlncomment = False
        for line in f:
            if re.search(ignore_pattern, line) == None:
                self.res[ex] += 1


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
    if len(sys.argv) < 1:
        print("Error, no arguments")
        print("[-path] [-extensions] {-a for all}")
        exit(1)

    dir = sys.argv[1]
    extensions = sys.argv[2:]
    counter = LinesCounter()
    print(counter.get_lines_count(dir, extensions))
