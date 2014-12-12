#!/usr/bin/env python

import re as regex

'''
Define Parameter
'''

class Parameter():
    '''Parameter'''

    def __init__(self, type_=None, name_=None, default_=None):
        self._type = type_
        self._name = name_
        self._default = default_

    def set_type(self, type_):
        self._type = type_

    def get_type(self):
        return self._type

    def set_name(self, name_):
        self._name = name_

    def get_name(self):
        return self._name

    def set_default(self, default_):
        self._default = default_

    def get_default(self):
        return self._default
        
    def is_empty(self):
        if self._type == None or self._name == None:
            return True 
        else:
            return False

    def to_string(self, is_print_default=False):
        if not self.is_empty():
            if self._default and is_print_default:
                return "%s %s=%s" % (self._type, self._name, self._default)
            else: 
                return "%s %s" % (self._type, self._name)

    def __str__(self):
        return self.to_string()

    def __nonzero__(self):
        return not self.is_empty()
     
    Regex = regex.compile(r'(.*)\b([A-Za-z_]\w*)')

    @staticmethod
    def Parse(param_string):
        temp = param_string.split('=')
        m = Parameter.Regex.match(temp[0])
        if m:
            type_str = m.group(1).strip()
            name_str = m.group(2).strip()
            default_str = None
            if len(temp) == 2:
                default_str = temp[1].strip()
            return Parameter(type_str, name_str, default_str)

def UnitTest():
    p = Parameter()
    assert(p.is_empty())
    p.set_type('const string &')
    assert(p.is_empty())
    p.set_name('name')
    assert(p.is_empty() == False)
    assert(str(p) == 'const string & name')
    assert(p)

    p = Parameter('vector<int*>', 'table')
    assert(not p.is_empty())
    assert(p.to_string() == "vector<int*> table")

    p = Parameter.Parse("vector<string> &str")

    assert(str(p) == "vector<string> & str")
    assert(p.get_type() == "vector<string> &")
    assert(p.get_name() == "str")

    p = Parameter.Parse('const string name="Unknow"')
    assert(p.get_type() == "const string")
    assert(p.get_name() == "name")
    assert(p.get_default() == '"Unknow"')

if __name__ == "__main__":
    UnitTest()
