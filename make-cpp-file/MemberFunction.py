#!/usr/bin/env python

from Function import *
import re as regex

class MemberFunction(Function):

    def __init__(self):
        Function.__init__(self)
        self._is_virtual = False
        self._class_name = ''

    def get_type(self):
        return FunctionType_Member

    def set_class_name(self, class_name):
        self._class_name = class_name

    def set_virtual(self, is_virtual_=True):
        self._is_virtual = is_virtual_

    def is_virtual(self):
        return self._is_virtual

    def is_vaild(self):
        if not Function.is_vaild(self):
            return False
        if self._class_name == None or self._class_name == '':
            return False
        return True

    def get_declare_string(self):
        if self.is_vaild():
            temp = ''
            if self._is_virtual:
                temp += 'virtual '
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
            temp += self._class_name + '::'
            temp += self._func_name + '('
            temp += self.get_params_string(False)
            temp += ')'
            if self._is_const:
                temp += ' const'
            return temp


    Regex = regex.compile(r'^\s*(?:virtual\s+)?(.*)\s+([A-Za-z_]\w*)\s*\((.*)\)(\s*const)?\s*;')
    CheckVirtualRegex = regex.compile(r'\bvirtual\b')

    @staticmethod
    def Parse(func_string):
        m = MemberFunction.Regex.match(func_string);
        if m != None:
            func_obj = MemberFunction()
            func_obj.set_return(m.group(1))
            func_obj.set_name(m.group(2))
            func_obj.set_params(GetParamList(m.group(3)))
            func_obj.set_const(m.group(4) != None)
            func_obj.set_virtual(MemberFunction.CheckVirtualRegex.match(func_string) != None)
            return func_obj
        pass

def MemberFunctionTest():
    test_str_list = []
    test_str_list.append("virtual const vector<int> & GetIDList() const;")
    test_str_list.append("const vector<int> & GetIDList() const;")
    test_str_list.append("void SetAge(int age);")
    test_str_list.append("void SetFileList(const vector<FileInfo> &fl, bool isSave=true);")
    test_str_list.append("void SetFileList(const vector<FileInfo> &fl);")
    for test_str in test_str_list:
        func_obj = MemberFunction.Parse(test_str)
        assert(func_obj != None)
        func_obj.set_class_name('CPerson')
        print func_obj.get_declare_string()
        print func_obj.get_implement_string()

#######################################################################################
class ConstructFunction(MemberFunction):
    def __init__(self):
        MemberFunction.__init__(self)

    def get_type(self):
        return FunctionType_Construct

    def is_vaild(self):
        if self._func_name == None:
            return False
        if self._func_name != self._class_name:
            return False
        if self._param_list != None:
            for param in self._param_list:
                if param != None and param.is_empty():
                    return False
        return True

    def get_declare_string(self):
        if self.is_vaild():
            temp = ''
            if self._is_virtual:
                temp += 'virtual '
            temp += self._func_name + '('
            temp += self.get_params_string(True)
            temp += ');'
            return temp

    def get_implement_string(self):
        if self.is_vaild():
            temp = self._class_name + '::'
            temp += self._func_name + '('
            temp += self.get_params_string(False)
            temp += ')'
            return temp

    Regex = regex.compile(r'^\s*(?:virtual\s+)?([A-Za-z_]\w*)\s*\((.*)\)\s*;')
    CheckVirtualRegex = regex.compile(r'\bvirtual\b')
    @staticmethod
    def Parse(func_string):
        m = ConstructFunction.Regex.match(func_string)
        if m != None :
            func_obj = ConstructFunction()
            func_obj.set_name(m.group(1))
            func_obj.set_params(GetParamList(m.group(2)))
            func_obj.set_virtual(MemberFunction.CheckVirtualRegex.match(func_string) != None)
            return func_obj
        pass

def ConstructFunctionTest():
    test_str_list = []
    test_str_list.append("virtual CPerson(const string &name , int age=-1);")
    test_str_list.append("CPerson();")
    for test_str in test_str_list:
        func_obj = ConstructFunction.Parse(test_str)
        assert(func_obj != None)
        func_obj.set_class_name('CPerson')
        print func_obj.get_declare_string()
        print func_obj.get_implement_string()


#######################################################################################
class DestructFunction(MemberFunction):
    def __init__(self):
        MemberFunction.__init__(self)

    def get_type(self):
        return FunctionType_Destruct

    def is_vaild(self):
        if self._func_name == None:
            return False
        if self._func_name != self._class_name:
            return False
        return True

    def get_declare_string(self):
        if self.is_vaild():
            temp = ''
            if self._is_virtual:
                temp += 'virtual '
            temp += '~' + self._func_name + '();'
            return temp

    def get_implement_string(self):
        if self.is_vaild():
            temp = '~' + self._class_name + '::'
            temp += self._func_name + '()'
            return temp

    Regex = regex.compile(r'^\s*(?:virtual\s+)?~\s*([A-Za-z_]\w*)\s*\(\s*\)\s*;')
    @staticmethod
    def Parse(func_string):
        m = DestructFunction.Regex.match(func_string)
        if m != None :
            func_obj = DestructFunction()
            func_obj.set_name(m.group(1))
            func_obj.set_virtual(MemberFunction.CheckVirtualRegex.match(func_string) != None)
            return func_obj
        pass

def DestructFunctionTest():
    test_str_list = []
    test_str_list.append("virtual ~CPerson( ) ;")
    test_str_list.append("~ CPerson();")
    for test_str in test_str_list:
        func_obj = DestructFunction.Parse(test_str)
        assert(func_obj != None)
        func_obj.set_class_name('CPerson')
        print func_obj.get_declare_string()
        print func_obj.get_implement_string()


if __name__ == "__main__":
    MemberFunctionTest()
    ConstructFunctionTest()
    DestructFunctionTest()
