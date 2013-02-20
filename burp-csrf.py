#!/usr/bin/env python

from __future__ import print_function
from lxml import etree, html
from lxml.html import builder as E
from base64 import b64decode
from urlparse import parse_qsl
import codecs

def process_file(input_file, output_file=None, encoding='utf-8'):
    if output_file is None:
        output_file = input_file + '.html'
    root = etree.parse(input_file).getroot()
    item = root.xpath("/items/item")[0]
    (method,) = item.xpath("method/text()")
    if method.lower() != "post":
        raise ValueError("Only POST requests are supported") # TODO
    (url,) = item.xpath("url/text()")
    (request,) = item.xpath("request")
    contents = request.text
    if request.get("base64"):
        contents = b64decode(contents)
    _, body = contents.split("\r\n\r\n", 1)
    output = E.HTML(
            E.HEAD(E.META(**{'http-equiv': 'Content-type',
                'content': 'text/html; charset=' + encoding})),
            E.BODY(
                E.FORM(
                    E.INPUT(type="submit"),
                    *(E.INPUT(type="hidden", name=name, value=value) for name, value
                        in decode_form_urlencoded_values(body, encoding)),
                    action=url, method=method
                    )
                )
            )
    with codecs.open(output_file, 'wb', encoding) as html_output:
        html_output.write(html.tostring(output, encoding=unicode))
    return output_file

def decode_form_urlencoded_values(request_body, encoding):
    for pair in parse_qsl(request_body, keep_blank_values=True):
        yield tuple(i.decode(encoding) for i in pair)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: {0} <file.xml>".format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)
    output_written = process_file(sys.argv[1])
    print('Output is ready in ' + output_written)
