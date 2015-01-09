# Module:  generator.py
# Author:  Abraham Yusuf <yabraham@swglobal.com>
# Created: Jan 8, 2015

import contextlib
import os
import random
import shutil
import sys
import xml.etree.ElementTree as ET

import config
from .config import get_config, get_file_count, get_test_cases


class DataGenerator(object):

    def __init__(self, src, dest=None):
        self.src = os.path.abspath(src)
        self.dest = os.path.abspath(dest or 'out')

    def gen_counts(self, folder, conf):
        # conf is instance of config.CountConfig
        pass

    def gen_dates(self, folder, conf):
        # conf is instance of config.DateConfig
        pass

    def gen_names(self, folder, conf):
        # conf is instance of config.NameConfig
        pass

    def gen_numbers(self, folder, conf):
        # conf is instance of config.NumberConfig
        xmlfiles = [
            os.path.join(folder, i) for i in os.listdir(folder)
            if i.endswith('.xml')
        ]
        mobile_nos = []

        while len(mobile_nos) != len(xmlfiles):
            base = random.randint(conf.range_start, conf.range_stop)
            mobile_no = '%s%s' % (conf.prefix, '{0:07d}'.format(base))
            if mobile_no not in mobile_nos:
                mobile_nos.append(mobile_no)

        for xmlfile in xmlfiles:
            with contextlib.closing(open(xmlfile)) as f:
                xmlstring = f.read()

            try:
                tree = ET.fromstring(xmlstring)
                tree.findall(
                    './/NigeriaSIMDemographics/MainMobileNumber'
                )[0].text = mobile_nos.pop()

                with contextlib.closing(open(xmlfile, 'w')) as f:
                    f.write(ET.tostring(tree, encoding='utf-8'))

            except Exception as e:
                print(e.message)
                continue

    def modify_fep_code(self, xmlfile):
        try:
            with contextlib.closing(open(xmlfile)) as f:
                xmldata = f.read()

            tree = ET.fromstring(xmldata)
            tree.findall('.//NigeriaSIMDemographics/FEPCode')[0].text = 'SWG'

            with contextlib.closing(open(xmlfile, 'w')) as f:
                f.write(ET.tostring(tree, encoding='utf-8'))

        except Exception as e:
            print(e.message)

    def run(self):
        self.split_files()

        for tc in get_test_cases():
            folder = os.path.join(self.dest, tc)
            conf = get_config(tc)

            if isinstance(conf, config.CountConfig):
                self.gen_counts(folder, conf)
            if isinstance(conf, config.DateConfig):
                self.gen_dates(folder, conf)
            if isinstance(conf, config.NameConfig):
                self.gen_names(folder, conf)
            if isinstance(conf, config.NumberConfig):
                self.gen_numbers(folder, conf)

    def split_files(self):
        print('re-arranging files according to test case...')

        min_file_count = get_file_count()
        xmlfiles = [i for i in os.listdir(self.src) if i.endswith('.xml')]

        if len(xmlfiles) < min_file_count:
            print(
                'Insufficient xml files. Found %s files, %s required.'
                % (len(xmlfiles), min_file_count)
            )
            sys.exit(1)

        for tc in get_test_cases():
            output_dir = os.path.join(self.dest, tc)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            for i in range(get_config(tc).file_count):
                srcfile = os.path.join(self.src, xmlfiles.pop())
                destfile = os.path.join(output_dir, '%s_%s.xml' % (tc, i))
                shutil.move(srcfile, destfile)
                self.modify_fep_code(destfile)

        print('done')
