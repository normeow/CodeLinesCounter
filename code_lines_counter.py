import sys
import os
import re

class LinesCounter:
    def __init__(self):
        #TODO don't forget about multilines comments
        self.ignorstr = {
            ".cpp" : "",
            ".java" : "",
            ".py" : "^{#\w*|import\w*|\n}$"
        }
        self.res = {}
        self.file_pattern = "\.(\w*)"

    def get_lines_count(self, dir, extns):
        self.res = dict.fromkeys(extns, 0)
        self.countlines(dir,extns)
        return self.res

    def count_lines_in_file(self, file, ex):
        f = open(file)
        ignore_pattern = self.ignorstr[ex]
        for line in f:
            if re.search(ignore_pattern, line) == None:
                self.res[ex] += 1


    def countlines(self, dir, extns):
        ls = os.listdir(dir)
        for it in ls:
            ex = re.search(self.file_pattern, it)
            if ex == None:
                self.countlines(dir+"/"+it, extns)
            elif ex.group(0) in extns:
                self.count_lines_in_file(dir+"/"+it, ex.group(0))

#TODO argparser

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Error, no arguments")
        print("[-path] [-extensions] {-a for all}")
        exit(1)

    dir = sys.argv[1]
    extensions = sys.argv[2:]
    counter = LinesCounter()
    print(counter.get_lines_count(dir, extensions))

#counter = LinesCounter()
#print(counter.get_lines_count("D://Code/hakerrank", [".py"]))

