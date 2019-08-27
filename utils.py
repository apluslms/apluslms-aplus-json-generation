import os
import sys
from io import BytesIO
import tarfile
import requests
from math import floor
from operator import itemgetter
import json, yaml


def url_to_static(static_url, course_key, path):
    """ Creates an URL for a path in static files """
    return '{}{}/{}'.format(static_url, course_key, path)


def update_url(static_url, course_key, data):
    """ Update static_content to url"""
    path = data.pop('static_content')
    if isinstance(path, dict):
        url = {
            lang: url_to_static(static_url, course_key, p)
            for lang, p in path.items()
        }
    else:
        url = url_to_static(static_url, course_key, path)

    data['url'] = url


def update_index_yaml(static_url, course_key, course_data):
    """ Update course data """
    def children_recursion(parent):
        if "children" in parent:
            for o in [o for o in parent["children"] if "key" in o]:
                if "static_content" in o:
                    update_url(static_url, course_key, o)
                children_recursion(o)

    if "modules" in course_data:
        for m in course_data["modules"]:
            children_recursion(m)


class ParseError(Exception):
    def __init__(self, value, error=None):
        self.value = value
        self.error = error

    def __str__(self):
        if self.error is not None:
            return "%s: %s" % (repr(self.value), repr(self.error))
        return repr(self.value)


class Parser:

    FORMATS = {
        'json': json.load,
        'yaml': yaml.safe_load,
        'yml': yaml.safe_load
    }

    def __init__(self, course_dir):
        '''
        The constructor.
        '''
        self._DIR = course_dir

    def parse(self, path, loader=None):
        '''
        Parses a dict from a file.
        @type path: C{str}
        @param path: a path to a file
        @type loader: C{function}
        @param loader: a configuration file stream parser
        @rtype: C{dict}
        @return: an object representing the configuration file or None
        '''
        if not loader:
            try:
                loader = self.FORMATS[os.path.splitext(path)[1][1:]]
            except:
                raise ParseError('Unsupported format "%s"' % path)
        data = None
        path = os.path.join(self._DIR, path)
        try:
            with open(path) as f:
                try:
                    data = loader(f)
                except ValueError as e:
                    raise ParseError("Configuration error in %s" % path, e)
        except OSError as e:
            print(e)

        return data


def error_print():
    return '{}. {}, line: {}'.format(sys.exc_info()[0],
                                     sys.exc_info()[1],
                                     sys.exc_info()[2].tb_lineno)




