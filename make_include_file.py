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

[2013-10-10 V1.0] create and first commit
[2013-10-11 V1.1] 
    (1) In last version the include path is ".././xxxx/xx.h". it should be
        "../xxxx/xx.h"
    (2) /*--aa.h--*/ in head file can't be recognized, but it works in 
        this version.
[2013-10-31 V1.2]
    Just changed the name of class_name_file and built_list_file
[2013-11-14 V1.3]
    (1) Optimazed load regEx, skip empty line.
    (2) Make it has ability to recognize "struct", "union", "enum" as well.
'''
import os
import re

output_include_path = 'inc'
tags_list_file = 'include_list'
built_list_file = '.include_list'

define_RegEx = '^\s*(?:class|struct|enum|union)\s+([A-Za-z_]\w*)'
declare_RegEx = '^\s*(?:class|struct|enum|union)\s+[A-Za-z_]\w*\s*;'
tag_RegEx = '^\s*/\*--\s*([A-Za-z0-9_\.]*)\s*--\*/'

tags_need_list = {}
built_file_list = []

def read_file_lines(file_name) :
    rfile = open(file_name, 'r')
    lines = rfile.readlines()
    rfile.close()
    return lines

def find_tag_in_line(line) :
    m = re.search(define_RegEx, line)
    if m : 
        if not re.search(declare_RegEx, line) : 
            return m.group(1)
    else :
        m = re.search(tag_RegEx, line)
        if m :
            return m.group(1)

def get_class_list_in_file(file_name) :
    class_list = []
    for line in read_file_lines(file_name) :
        class_name = find_tag_in_line(line)
        if class_name :
            class_list.append(class_name)
    return class_list

def build_class_include_file(class_name, file_name) : 
    context = '#include "../%s"\n' % file_name[2:]
    built_file_list.append(class_name)
    wfile = open("./%s/%s" % (output_include_path, class_name), "a")
    wfile.write(context)
    wfile.close()

def do_head_file(file_name) :
    class_list = get_class_list_in_file(file_name)
    for class_name in class_list :
        if class_name in tags_need_list :
            build_class_include_file(class_name, file_name)
            tags_need_list[class_name] += 1
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

    for class_name in tags_need_list :
        count = tags_need_list[class_name]
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
    if not os.path.exists(tags_list_file) :
        print 'ERROR: need ', tags_list_file
        quit()

    for line in read_file_lines(tags_list_file) :
        line = line.strip('\n')
        if re.match('^\s*#', line) : continue
        if re.match('^\s*[A-Za-z0-9_\.]+\s*$', line) :
            tags_need_list[line.strip()] = 0

if __name__ == "__main__" :
    clear()
    load()
    build()
    summarize()
