# Module:  main.py
# Author:  Abraham Yusuf <yabraham@swglobal.com>
# Created: Jan 8, 2015

import os
import sys

from generator import DataGenerator


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py src [dest]')
        sys.exit(1)

    src = os.path.abspath(sys.argv[1])
    dest = os.path.abspath(sys.argv[2]) if len(sys.argv) >= 3 else 'out'

    if not os.path.exists(src):
        print('src directory does not exist')
        sys.exit(1)

    if not os.path.exists(dest):
        os.mkdir(dest)

    DataGenerator(src, dest).run()
    print('Ce Fin!')

if __name__ == '__main__':
    main()
