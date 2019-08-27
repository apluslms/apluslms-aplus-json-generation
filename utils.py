import os
import sys
from io import BytesIO
import tarfile
import requests
from math import floor
from operator import itemgetter


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


def error_print():
    return '{}. {}, line: {}'.format(sys.exc_info()[0],
                                     sys.exc_info()[1],
                                     sys.exc_info()[2].tb_lineno)




