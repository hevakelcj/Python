#!/usr/bin/env python
#coding=utf-8

''' 
This script is due to build class include file in ./inc/
It finds all head file in current path, fetch class name define in
each head files. If this class is specified in class_list.in Then, 
create a file name as class name in ./inc/, put C/C++ include string 
inside.

File    : make_include_file.py
Author  : Chunjun Li <hevakelcj@gmail.com>
Date    : 2013-10-05
'''
import os
import re

output_include_path = 'inc'
built_list_file = 'class_list.out'
class_need_file = 'class_list.in'

class_need_list = {}
built_file_list = []

def read_file_lines(file_name) :
    rfile = open(file_name, 'r')
    lines = rfile.readlines()
    rfile.close()
    return lines

def find_class_define_in_line(line) :
    m = re.search('^\s*class\s+([A-Za-z_]\w*)', line)
    if m : 
        if not re.search('^\s*class\s+[A-Za-z_]\w*\s*;', line) : 
            return m.group(1)
    else :
        m = re.search('^/\*--([A-Za-z_]\w*)--\*/', line)
        if m :
            return m.group(1)

def get_class_list_in_file(file_name) :
    class_list = []
    for line in read_file_lines(file_name) :
        class_name = find_class_define_in_line(line)
        if class_name :
            class_list.append(class_name)
    return class_list

def build_class_include_file(class_name, file_name) : 
    context = '#include "../%s"\n' % file_name
    built_file_list.append(class_name)
    wfile = open("./%s/%s" % (output_include_path, class_name), "a")
    wfile.write(context)
    wfile.close()

def do_head_file(file_name) :
    class_list = get_class_list_in_file(file_name)
    for class_name in class_list :
        if class_name in class_need_list :
            build_class_include_file(class_name, file_name)
            class_need_list[class_name] += 1
            #print "%s --> %s" % (class_name, file_name)

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

    wfile = open('./%s/%s' % (output_include_path, built_list_file), 'w')
    for built_file in built_file_list :
        wfile.write(built_file + '\n')
    wfile.close()

def summarize() :
    undo, done, more = '', '', ''

    for class_name in class_need_list :
        count = class_need_list[class_name]
        if count == 0 : 
            undo += (class_name + ' ')
        elif count > 1 : 
            more += (class_name + ' ')
        else :
            done += (class_name + ' ')

    print '-' * 80
    if done != '' :
        print '[DONE]:\n', done, '\n'
    if more != '' :
        print '[FOUND MORE THAN ONCE]:\n', more, '\n'
    if undo != '' :
        print '[NOT FOUND]:\n', undo, '\n'

def clear() :
    if not os.path.exists(output_include_path) :
        os.mkdir(output_include_path)
        return

    list_file = './%s/%s' % (output_include_path, built_list_file)
    if not os.path.exists(list_file) :
        return 

    for line in read_file_lines(list_file) :
        file_name = './%s/%s' % (output_include_path, line.strip('\n'))
        if os.path.exists(file_name) :
            os.remove(file_name)

    os.remove(list_file)

def load() :
    if not os.path.exists(class_need_file) :
        print 'ERROR: need ', class_need_file
        quit()

    for line in read_file_lines(class_need_file) :
        line = line.strip('\n')
        if re.match('^#', line) : continue
        if re.match('^[A-Za-z_]\w*$', line) :
            class_need_list[line] = 0

if __name__ == "__main__" :
    clear()
    load()
    build()
    summarize()
