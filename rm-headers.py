#!/usr/bin/env python

from __future__ import print_function, with_statement
from mmap import mmap, ACCESS_READ
from shutil import copyfileobj
from contextlib import closing
from sys import stderr
from os import path, SEEK_SET

SEPARATOR = '\r\n\r\n'

def process(files):
    for file_name in files:
        output_name = file_name + '.nohead'
        if path.exists(output_name):
            print('{0} already exists, skipping {1}'.format(output_name,
                file_name), file=stderr)
            continue
        found_header = False
        with file(file_name, 'rb') as http_resp:
            with file(output_name, 'wb') as output:
                with closing(mmap(http_resp.fileno(), 0, access=ACCESS_READ)) as http_resp_mmap:
                    pos = http_resp_mmap.find(SEPARATOR)
                if pos >= 0:
                    http_resp.seek(pos + len(SEPARATOR), SEEK_SET)
                copyfileobj(http_resp, output)


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        print('Usage: {0} file1 [file2] ...'.format(argv[0]), file=stderr)
    else:
        process(argv[1:])
