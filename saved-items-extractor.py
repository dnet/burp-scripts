#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from base64 import b64decode
from lxml import etree

def process_file(input_file):
    items = etree.parse(input_file).getroot()
    pad = len(str(len(items)))
    for n, item in enumerate(items):
        for path in ["request", "response"]:
            (payload,) = item.xpath(path)
            contents = payload.text
            if payload.get("base64"):
                contents = b64decode(contents)
            with open('{0}{1:0{2}}.http'.format(path, n, pad), 'w') as f:
                f.write(contents)

if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 2:
        print("Usage: {0} <file.xml> [output.csv]".format(argv[0]), file=stderr)
        raise SystemExit(1)
    process_file(argv[1])
