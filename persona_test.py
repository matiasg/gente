#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import persona

class TestPersona(unittest.TestCase):
    def test1(self):
        p = persona.Persona(tel='15-1123-3321')
        d = p.get_data()
        self.assertEqual('15-1123-3321', d['tel'])
        self.assertEqual(1, len(d))

    def test_fonos(self):
        p = persona.Persona(tel='15-1123-3321')
        t = p.get_phones()
        self.assertEqual(1, len(t))

    def test_fonos2(self):
        p = persona.Persona()
        p.add_data('15-1123-3321')
        t = p.get_phones()
        self.assertEqual(1, len(t))
        self.assertTrue('15-1123-3321' in t)
        self.assertEqual('15-1123-3321', p.get_mobile())
        p.add_data('4423-3321')
        t = p.get_phones()
        self.assertEqual(2, len(t))
        self.assertTrue('4423-3321' in t)
        self.assertEqual('15-1123-3321', p.get_mobile())

    def test_fonos3(self):
        p = persona.Persona()
        p.add_data('(54-11) 4343-3434')
        t = p.get_phones()
        self.assertEqual(1, len(t))
        self.assertTrue('(54-11) 4343-3434' in t)


    def test_address(self):
        p = persona.Persona()
        p.add_data('San Martin 1212 4 C')
        t = p.get_address()
        self.assertEqual(1, len(t))
        self.assertEqual('San Martin 1212 4 C', t[0])
        p.add_data('San Juan 1212 PB')
        t = p.get_address()
        self.assertEqual(2, len(t))
        self.assertEqual('San Juan 1212 PB', t[1])

    def test_email(self):
        p = persona.Persona()
        p.add_data('juan_gil.1980@gmail.com')
        t = p.get_address()
        self.assertEqual('', t)
        t = p.get_email()
        self.assertEqual(1, len(t))
        self.assertEqual('juan_gil.1980@gmail.com', t[0])
        p.add_data('jg.magilquenunca@hotmail.com')
        t = p.get_email()
        self.assertEqual(2, len(t))

if __name__ == "__main__":
    unittest.main()
