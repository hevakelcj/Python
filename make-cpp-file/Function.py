#!/usr/bin/env python

import re as regex
from Parameter import *

class FunctionType:
    FunctionType_Normal = 1
    FunctionType_Member = 2 
    FunctionType_Construct = 3 
    FunctionType_Destruct = 4 

def GetParamList(param_list_str):
    param_list = []
    for param_str in param_list_str.split(','):
        param = Parameter.Parse(param_str.strip())
        param_list.append(param)
    return param_list

class Function:

    def __init__(self, name_=None):
        self._func_name = name_
        self._param_list = []
        self._return = None
        self._is_const = False

    def get_type():
        return FunctionType_Normal

    def set_name(self, name_):
        self._func_name = name_

    def add_param(self, param):
        self._param_list.append(param)

    def set_params(self, params):
        self._param_list = params

    def set_return(self, return_):
        self._return = return_

    def set_const(self, is_const_=True):
        self._is_const = is_const_

    def is_vaild(self):
        if self._func_name == None:
            return False
        if self._return == None:
            return False

        if self._param_list != None:
            for param in self._param_list:
                if param != None and param.is_empty():
                    return False

        return True

    def get_params_string(self, isHasInitValue):
        temp = ''
        for i in range(len(self._param_list)):
            param = self._param_list[i]
            if param != None:
                temp += param.to_string(isHasInitValue)
            if i < len(self._param_list) - 1:
                temp += ', '
        return temp

    def get_empty_body(self):
        temp += '{\n'
        for param in self._param_list:
            temp += '    (void)' + param.get_name() + ';\n'
        if self._return and self._return != 'void':
            temp += '    return ' + self._return + '();\n'
        temp += '}'

    def get_declare_string(self):
        if self.is_vaild():
            temp = ''
            if self._return:
                temp += self._return + ' '

            temp += self._func_name + '('
            temp += self.get_params_string(True)
            temp += ')'
            if self._is_const:
                temp += ' const'
            temp += ';'
            return temp

    def get_implement_string(self):
        if self.is_vaild():
            temp = self._return + ' '
            temp += self._func_name + '('
            temp += self.get_params_string(False)
            temp += ')'
            if self._is_const:
                temp += ' const'
            return temp

    Regex = regex.compile(r'^\s*(.*)\s+([A-Za-z_]\w*)\((.*)\)(\s*const)?\s*;')

    @staticmethod
    def Parse(func_string):
        m = Function.Regex.match(func_string);
        if m:
            ret_type = m.group(1)
            func_name = m.group(2)
            param_list = m.group(3)
            is_const = m.group(4) != None

            func_obj = Function(func_name)
            func_obj.set_const(is_const)
            func_obj.set_return(ret_type)
            func_obj.set_params(GetParamList(param_list))

            return func_obj

#############################################################

def TestMakeFunc(func_str):
    f = Function.Parse(func_str);
    assert(f)
    print '-' * 50
    print func_str
    print f.get_declare_string()
    print f.get_implement_string()

if __name__ == "__main__":
    func_str='int SetLine(const string name = "NoName", LineStyle style, int width=1, COLOR color = 0xffff00) const;'
    TestMakeFunc(func_str)

    func_str='Painter& SetLine(const vector<int> &vStyle) const;'
    TestMakeFunc(func_str)

    func_str='const Painter& SetLine(const vector<int> &vStyle);'
    TestMakeFunc(func_str)

    func_str='int GetAge();'
    TestMakeFunc(func_str)

