# Module:  generator.py
# Author:  Abraham Yusuf <yabraham@swglobal.com>
# Created: Jan 8, 2015

import os
import random
import shutil
import sys
import xml.etree.ElementTree as ET

import config
from config import get_config, get_file_count, get_test_cases
from helper import *


class DataGenerator(object):

    def __init__(self, src, dest=None):
        self.src = os.path.abspath(src)
        self.dest = os.path.abspath(dest or 'out')

    def gen_counts(self, folder, conf):
        # conf is instance of config.CountConfig
        print('generating data for mobile number counts...')
        xmlfiles = get_xml_files(folder)

        for xmlfile in xmlfiles:
            document = read_xml(xmlfile)
            if document is not None:
                remove_elems(document)
                mobile_nos = mk_numbers(
                    conf.add_count - 1, 0, 9999999
                )

                parent = document.find('NigeriaSIMDemographics')
                if parent is not None:
                    for i in range(2, conf.add_count + 1):
                        tag = 'MobileNumber%s' % i
                        elem = ET.SubElement(parent, tag)
                        elem.text = '%s' % mobile_nos.pop()

            write_xml(xmlfile, document)

        print('done')

    def gen_dates(self, folder, conf):
        # conf is instance of config.DateConfig
        print('generating data for dates of birth...')
        for xmlfile in get_xml_files(folder):
            document = read_xml(xmlfile)
            if document is not None:
                dob = document.find('.//NigeriaSIMDemographics/DateOfBirth')
                yymmdd = [
                    random.randint(conf.range_start, conf.range_stop)
                ]
                yymmdd.extend(dob.text.split('-')[1:])

                dob.text = '-'.join(map(str, yymmdd))

            write_xml(xmlfile, document)
        print('done')

    def gen_names(self, folder, conf):
        # conf is instance of config.NameConfig
        print('generating data for names...')

        for xmlfile in get_xml_files(folder):
            document = read_xml(xmlfile)
            if document is not None:
                parent = document.find('NigeriaSIMDemographics')

            if parent is not None:
                parent.find(conf.search).text = mk_name(conf.type_)

            write_xml(xmlfile, document)

        print('done')

    def gen_numbers(self, folder, conf):
        # conf is instance of config.NumberConfig
        print('generating test data for mobile numbers by MNO..')
        xmlfiles = get_xml_files(folder)
        mobile_nos = mk_numbers(
            len(xmlfiles), conf.range_start, conf.range_stop, conf.prefix
        )

        for xmlfile in xmlfiles:
            document = read_xml(xmlfile)
            if document is not None:
                document.find(
                    './/NigeriaSIMDemographics/MainMobileNumber'
                ).text = mobile_nos.pop()

                write_xml(xmlfile, document)

        print('done')

    def modify_fep_code(self, xmlfile):
        document = read_xml(xmlfile)
        if document is not None:
            document.find('.//NigeriaSIMDemographics/FEPCode').text = 'SWG'
            write_xml(xmlfile, document)

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
        xmlfiles = get_xml_files(self.src)

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
                srcfile = xmlfiles.pop()
                destfile = os.path.join(
                    output_dir, '%s_%s.xml' % (tc, '{0:04d}'.format(i))
                )
                shutil.move(srcfile, destfile)
                self.modify_fep_code(destfile)

        print('done')
