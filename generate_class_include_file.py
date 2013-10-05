#!/usr/bin/env python
#coding=utf-8

''' 
This script is due to build class include file in ./inc/
It finds all head file in current path, pick out all class name define in
each head files. Then, create a file name as class name in ./inc/, put 
C/C++ include string inside.
Instance:
    In head file ./src/Job.h, there are two class defined inside: Teacher,
    Doctor, Engineer.
    It will create Teacher,Doctor,Engineer in ./inc/, and put:
        #include ".././src/Job.h"
    in each file.

Author  : Chunjun Li <hevakelcj@gmail.com>
Date    : 2013-10-05
'''
import os
import re

def find_class_define_in_line(line) :
    '''
    Use regular expresss to check is there define a class in this line
    ignore class declare.
    '''
    m = re.search('^\s*class\s+([A-Za-z_]\w*)', line)
    if m : 
        if not re.search('^\s*class\s+[A-Za-z_]\w*\s*;', line) : 
            return m.group(1)

def get_class_list_in_file(file_name) :
    class_list = []
    rfile = open(file_name, "r")
    while True :
        line = rfile.readline()
        if not line : 
            break
        class_name = find_class_define_in_line(line)
        if class_name :
            class_list.append(class_name)
    rfile.close()
    return class_list

def build_class_include_file(class_name, file_name) : 
    context = '#include "../%s"\n' % file_name
    wfile = open("./inc/%s" % (class_name), "a")
    wfile.write(context)
    wfile.close()

def do_head_file(file_name) :
    class_list = get_class_list_in_file(file_name)
    for class_name in class_list :
        build_class_include_file(class_name, file_name)
        print "%s --> %s" % (class_name, file_name)

def find_head_files(path) :
    tmp = os.popen('find %s -type f -name "*.hpp" -o -name "*.h"' % (path))
    file_list = []
    for line in tmp.readlines():
        file_list.append(line.strip('\n'))
    return file_list

def build() :
    file_list = find_head_files("./")
    for file_name in file_list : 
        do_head_file(file_name)

if __name__ == "__main__" :
    if os.path.exists('inc') :
        os.system('rm -rf inc')
    os.mkdir('inc')
    build()
