# Module:  helper.py
# Author:  Abraham Yusuf <yabraham@swglobal.com>
# Created: Jan 12, 2015

import contextlib
import os
import random
import re
import xml.etree.ElementTree as ET


def mk_name(type_):
    alpha = 'ABCDEFGHIJKLMOPQRSTUVWXYZ'
    digits = '0123456789'
    if type_ == 'blank':
        return ''
    elif type_ == 'one':
        return random.choice(alpha)
    elif type_ == 'number':
        return '%s' % random.randint(1000, 99999999)
    elif type_ == 'mixed':
        length = random.randrange(5, 10)
        strr = ''
        while len(strr) < length:
            if random.choice([1, 0]) == 1:
                nextchar = random.choice(alpha)
            else:
                nextchar = random.choice(digits)
            strr = '%s%s' % (strr, nextchar)
        return strr
    else:
        raise Exception('Unknown type [%s]' % type_)


def mk_numbers(count, start, stop, prefix=None):
    prefs = [
        802, 803, 805, 806, 807, 809, 810, 812, 813, 814, 815, 816, 817
    ]
    mobile_nos = []

    while len(mobile_nos) < count:
        base = random.randint(start, stop)
        p = prefix if prefix else random.choice(prefs)
        mobile_no = '%s%s' % (p, '{0:07d}'.format(base))

        if mobile_no not in mobile_nos:
            mobile_nos.append(mobile_no)

    return mobile_nos


def remove_elems(root):
    pattern = re.compile('^MobileNumber\d+$')
    mobile_num_elems = []

    parent = root.find('NigeriaSIMDemographics')
    if parent is not None:
        for elem in parent.iter():
            if re.search(pattern, elem.tag):
                mobile_num_elems.append(elem.tag)

        for tag_name in mobile_num_elems:
            parent.remove(parent.find(tag_name))


def get_xml_files(folder):
    return [
        os.path.join(folder, i) for i in os.listdir(folder)
        if i.endswith('.xml')
    ]


def read_xml(xmlfile):
    try:
        with contextlib.closing(open(xmlfile)) as f:
            xmlstring = f.read()

        document = ET.fromstring(xmlstring)
        return document
    except Exception:
        return None


def write_xml(filename, document):
    try:
        with contextlib.closing(open(filename, 'w')) as f:
            f.write(ET.tostring(document, encoding='utf-8'))
    except Exception as e:
        print(e.message)
