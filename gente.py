#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, os
from optparse import OptionParser
from subprocess import Popen, PIPE
import tempfile
import persona

EDITOR = 'vim'

def normalize(word):
    normfrom = u'áéíóúü'
    normto = u'aeiouu'
    for i in range(len(normfrom)):
        word = word.replace(normfrom[i], normto[i])
    return word

def letter_distance(l, m):
    l = normalize(l.lower())
    m = normalize(m.lower())
    if l==m:
        return 0
    return 1

def levenshtein_with_insertions(needle, objective):
    dist = [[0 for j in range(1+len(objective))] for i in range(1+len(needle))]
    for i in xrange(1,1+len(needle)):
        dist[i][0] = i
        for j in xrange(1,1+len(objective)):
            dist[i][j] = min(
                    dist[i][j-1] + 1,
                    dist[i-1][j-1] + letter_distance(needle[i-1], objective[j-1]),
                    dist[i-1][j] + 1)
    return min(dist[len(needle)][j] for j in range(1+len(objective)))

def read_vcard(file):
    ret = ''
    fields_to_save = 'FN TEL ADR'.split()
    with open(file, 'r') as f:
        for line in f:
            lisp = line.strip().split(':')
            for field in fields_to_save:
                if field in lisp[0]:
                    ret += lisp[1].strip(';') + '|'
    return ret[:-1]


class gente:
    def __init__(self, FILE):
        self.SEP = '|'
        self.FILE = FILE
        f = open(self.FILE, 'r')
        bk = f.readlines()
        f.close()
        self.book = [p.decode('utf-8').strip() for p in bk]

    def saveonfile(self, file=''):
        if file=='':
            file = self.FILE
        f = open(file, 'w')
        for pe in sorted(self.book, cmp = lambda x,y : cmp(x.lower(), y.lower())):
            f.write(pe.encode('utf-8')+'\n')
        f.close()

    def makebackup(self):
        self.saveonfile(self.FILE+".bu")

    def printperson(self,per):
        for i in per.split(self.SEP):
            print i

    def getperson(self, needle):
        ret = self.lookfor_exact(needle)
        if ret == []:
            ret,dist = self.get_close_people(needle)
            if dist:
                print "There were no exact matches. Printing results at distance %s.\n" % dist
        for i,l in enumerate(ret):
            print '-' * 40, i+1 # people like 1-based numerations. I guess :S
            self.printperson(l)

    def lookfor_exact(self, needle):
        ne = re.compile("(?i)"+needle)
        ret = [l for l in self.book if ne.search(l)]
        return ret

    def get_close_people(self, needle):
        newlist = sorted([[levenshtein_with_insertions(needle, p), p] for p in self.book])
        mindist = newlist[0][0]
        return [p for d,p in newlist if d == mindist], mindist

    def removeperson(self, needle):
        ne = re.compile("(?i)"+needle)
        for p in self.book:
            if ne.search(p):
                print 'Do you want to remove this person?'
                self.printperson(p)
                answer = raw_input('yN: ')
                if answer.lower() == 'y':
                    self.book.remove(p)
        self.saveonfile()

    def editperson(self, needle):
        global EDITOR
        newbook = []
        delfrombook = []
        ne = re.compile("(?i)"+needle)
        for p in self.book:
            if ne.search(p):
                print 'Do you want to edit this person?'
                self.printperson(p)
                answer = raw_input('yN: ')
                if answer.lower() == 'y':
                    delfrombook.append(p)
                    f = tempfile.NamedTemporaryFile(delete=False)
                    f.write(re.sub('\|','\n',p.encode('utf8')))
                    f.flush()
                    lsplit = (EDITOR+' '+f.name).split()
                    p = Popen(lsplit)
                    d = p.communicate()[0]
                    f.close()
                    fagain = open(f.name, 'r')
                    person = '|'.join([l.strip() for l in fagain.readlines()])
                    fagain.close()
                    print person
                    #os.unlink(f.name)
                    newbook.append(person.decode('utf8'))
        for p in delfrombook:
            self.book.remove(p)
        self.book.extend(newbook)
        self.makebackup()
        self.saveonfile()

    def saveperson(self, person):
        self.book.append(person)
        self.makebackup()
        self.saveonfile()

    def ask_person_with_editor(self):
        global EDITOR
        f = tempfile.NamedTemporaryFile(delete=False)
        lsplit = (EDITOR+' '+f.name).split()
        p = Popen(lsplit)
        d = p.communicate()[0]
        person = '|'.join([l.strip() for l in f.readlines()])
        os.unlink(f.name)
        return person

    def askForPerson(self):
        print "Enter person data. Finish with an empty line."
        ret = ""
        while 1:
            try:
                li = raw_input()
            except:
                break
            if li == "":
                break
            ret += (li + "|")
        return ret

    def dump_to_csv(self, file='lista_dump.csv'):
        with open(file, 'w') as f:
            f.write(persona.csv_header())
            for p in self.book:
                pspl = p.split(self.SEP)
                per = persona.Persona(*pspl)
                #per.set_name(pspl[0])
                #for d in pspl:
                #    per.add_data(d)
                perline = per.csv_line()
                if perline:
                    f.write(per.csv_line().encode('utf8'))



if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store", dest="file", help="file with gente")
    parser.add_option("-s", "--search", action="store", dest="person", help="look for person")
    parser.add_option("-n", "--new", action="store_true", dest="newperson", help="enter new person")
    parser.add_option("-v", "--vcard", action="store", dest="vcard_file", help="enter new person from vcard")
    parser.add_option("-d", "--delete", action="store", dest="persontodel", help="delete person")
    parser.add_option("-t", "--test", action="store_true", dest="testing", help="just testing")
    parser.add_option("-e", "--edit", action="store", dest="persontoedit", help="edit a person")
    parser.add_option("-m", "--dump", action="store_true", dest="dump_to_csv", help="dump gente to a csv file")
    (options, args) = parser.parse_args()
    if options.file:
        FILE = options.file
    else:
        FILE = os.path.join(os.environ.get('HOME'), '.gente')
    contactos = gente(FILE)
    if options.testing:
        contactos.ask_person_with_editor()
        sys.exit()

    if options.person:
        contactos.getperson(options.person.decode('utf-8'))
    elif options.newperson:
        #person = contactos.askForPerson().decode('utf-8')
        person = contactos.ask_person_with_editor().decode('utf-8')
        contactos.saveperson(person)
    elif options.persontodel:
        contactos.removeperson(options.persontodel)
    elif options.vcard_file:
        person = read_vcard(options.vcard_file)
        contactos.saveperson(person.decode('utf8'))
    elif options.persontoedit:
        contactos.editperson(options.persontoedit)
    elif options.dump_to_csv:
        contactos.dump_to_csv()

