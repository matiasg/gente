#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
kphone = re.compile('(?i)phone|tel|mobile')
vphone = re.compile('^(\([\d\s-]*\))?[\d\s-]*$')
vcell = re.compile('^\s*15')
vaddress = re.compile('^[\s\w]*\s*\d+\s*(\d*\s*[a-zA-Z]*)\s*$')
vemail = re.compile('[\w\.]*@\w*(\.\w*)+')

name_key = u'Name'
cell_key = u'Mobile Phone'
phon_key = u'Home Phone'
addr_key = u'Home Address'
emai_key = u'E-mail Address'
fmt = u'{n},{c},{p},{a},{e}\n'

def csv_header():
    return fmt.format(n=name_key, c=cell_key, p=phon_key, a=addr_key, e=emai_key)

class Persona(object):
    def __init__(self, *args, **kwargs):
        self.data = kwargs
        for k in [name_key, cell_key, phon_key, addr_key, emai_key]:
            if not self.data.has_key(k):
                self.data[k] = []
        self.set_name(args[0])
        for d in args[1:]:
            self.add_data(d)
    def print_data(self):
        print self.data
    def get_data(self):
        return self.data
    def get_mobile(self):
        return self.data.get(cell_key,'')
    def get_phones(self):
        ret = []
        for k,v in self.data.iteritems():
            if kphone.search(k):
                ret.append(v)
        return ret
    def get_address(self):
        return self.data.get(addr_key, '')
    def get_email(self):
        return self.data.get(emai_key, '')
    def csv_line(self):
        if not self.data[name_key]:
            return None
        if not (self.data[cell_key] or self.data[phon_key] or self.data[addr_key] or self.data[emai_key]):
            return None
        return fmt.format(n=self.data.get(name_key),
                         c=':'.join(self.data[cell_key]),
                         p=':'.join(self.data[phon_key]),
                         a=':'.join(self.data[addr_key]),
                         e=':'.join(self.data[emai_key]))
    def set_name(self, name):
        self.data[name_key] = name
    def add_data(self, some_data):
        if vphone.search(some_data):
            if vcell.search(some_data):
                k = cell_key
            else:
                k = phon_key
            tf = self.data.get(k, '')
            self.data[k].append(some_data)
        elif vaddress.search(some_data):
            self.data[addr_key].append(some_data)
        elif vemail.search(some_data):
            self.data[emai_key].append(some_data)


