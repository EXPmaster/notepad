# -*- coding: utf-8 -*-
# coding = utf-8
#! /usr/bin/env python3

# ptags
#
# Create a tags file for Python programs, usable with vi.
# Tagged are:
# - functions (even inside other defs or classes)
# - classes
# - filenames
# Warns about files it cannot open.
# No warnings about duplicate tags.

import sys, re, os
import subprocess
import argparse

tags = []    # Modified global variable!
def parse_args():
    parser = argparse.ArgumentParser(description='dir_path')
    parser.add_argument('--path',
                    help='current dir path',
                    required=True,
                    type=str)

def main():
    subprocess.Popen(["dir", "*.py", "/s", '/b', '>', 'pythonfile.txt'], stdout=subprocess.PIPE, shell=True)
    with open('pythonfile.txt', 'r') as fr:
        files = fr.readlines()
    # print(files)
    for filename in files:
        treat_file(filename)
    if tags:
        fp = open('tags', 'w')
        tags.sort()
        for s in tags: fp.write(s)


expr = r'^[ \t]*(def|class)[ \t]+([a-zA-Z0-9_]+)[ \t]*[:\(]'
matcher = re.compile(expr)

def treat_file(filename):
    filename = '/'.join(filename.split('\\'))
    filename = filename[:-1]
    try:
        fp = open(filename, 'r', encoding='utf-8')
    except:
        sys.stderr.write('Cannot open %s\n' % filename)
        return
    base = os.path.basename(filename)
    if base[-3:] == '.py':
        base = base[:-3]
    s = base + '\t' + filename + '\t' + '1\n'
    tags.append(s)
    while 1:
        line = fp.readline()
        if not line:
            break
        m = matcher.match(line)
        if m:
            content = m.group(0)
            name = m.group(2)
            s = name + '\t' + filename + '\t/^' + content + '/\n'
            tags.append(s)

if __name__ == '__main__':
    main()
