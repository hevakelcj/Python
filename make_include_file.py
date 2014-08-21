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
[2014-08-21 V1.4]
    Problem:
        If it remove all file it made before, our project will rebuild a lot
        of source again. It's time-consuming.
    Solution:
        It will not remove all include files before run. 
        Make all new include files in temp directory. Then compare them with
        old files. If two file is the same. It will not modify them.
'''
import os
import re
import filecmp

output_include_path = 'inc'
temp_output_include_path = 'temp_inc'

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
    wfile = open("./%s/%s" % (temp_output_include_path, class_name), "a")
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

    wfile = open('./%s/%s' % (temp_output_include_path, built_list_file), 'w')
    for built_file in built_file_list :
        wfile.write(built_file + '\n')
    wfile.close()

def report() :
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
    if more != '' :
        print '[FOUND MORE THAN ONCE]:\n', more, '\n'
    if undo != '' :
        print '[NOT FOUND]:\n', undo, '\n'

def prepare():
    if not os.path.exists(output_include_path):
        os.mkdir(output_include_path)
    if not os.path.exists(temp_output_include_path):
        os.mkdir(temp_output_include_path)

def load() :
    if not os.path.exists(tags_list_file) :
        print 'ERROR: need ', tags_list_file
        quit()

    for line in read_file_lines(tags_list_file) :
        line = line.strip('\n')
        if re.match('^\s*#', line) : continue
        if re.match('^\s*[A-Za-z0-9_\.]+\s*$', line) :
            tags_need_list[line.strip()] = 0

def check():
    inc_build_list_file = output_include_path+'/'+built_list_file
    files_in_inc_dir = []
    if os.path.exists(inc_build_list_file):
        lines = read_file_lines(inc_build_list_file)
        for l in lines:
            files_in_inc_dir.append(l.strip())
        files_in_inc_dir.append(built_list_file)


    files_in_tmp_dir = os.listdir(temp_output_include_path)
     
    for f in files_in_inc_dir:
        if not f in files_in_tmp_dir:
            os.remove(output_include_path+'/'+f)
            print "D\t", f

    for f in files_in_tmp_dir:
        tmp_file = temp_output_include_path + '/' + f;
        inc_file = output_include_path + '/' + f;
        if not f in files_in_inc_dir:
            os.rename(tmp_file, inc_file)
            print 'A\t', f
        elif not filecmp.cmp(tmp_file, inc_file):
            os.rename(tmp_file, inc_file)
            print "M\t", f
        else:
            os.remove(tmp_file)

    os.removedirs(temp_output_include_path)
    pass

if __name__ == "__main__" :
    prepare()
    load()
    build()
    check()
    report()
