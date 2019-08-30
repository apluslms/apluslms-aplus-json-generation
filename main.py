import os
import json
import requests

from apluslms_yamlidator.validator import Validator
from course import Course
from parser import yaml
from utils import aplus_json


if __name__ == "__main__":

    generated_dir = 'generated/'

    # Set up validator
    validator = Validator(dirs=['schemas'])
    _v, ref = validator.get_version('index', 1)
    schema = validator.get_schema(ref)
    with open(generated_dir+"schema.json", "w") as schema_json:
        json.dump(schema, schema_json, indent=4, sort_keys=True)

    # Load and parse course index.yaml
    COURSE_DIR = os.getcwd()
    course = Course(COURSE_DIR)
    course.load('index.yaml')
    course_data = course.get_data()
    with open(generated_dir+"course.json", "w") as course_json:
        json.dump(course_data, course_json, indent=4, sort_keys=True)

    # Validate index.yaml
    if not validator.validate(course_data, 'index', major=1):
        raise ValueError('Invalid index.yaml')

    os.environ['PLUGIN_API'] = 'http://0.0.0.0:8080/api/v1/'
    os.environ['PLUGIN_TOKEN'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkZWZfY291cnNlIiwiaWF0IjoxNTYyODI4MzA0L' \
                                 'CJpc3MiOiJzaGVwaGVyZCJ9.MUkoD27P6qZKKMM5juL0e0pZl8OVH6S17N_ZFzC7D0cwOgbcDaAO3S1BauXzhQ' \
                                 'OneChPs1KEzUxI2dVF-Od_gpN8_IJEnQnk25XmZYecfdoJ5ST-6YonVmUMzKP7UAcvzCFye7mkX7zJ1ADYtda5' \
                                 '7IUdyaLSPOWnFBSHX5B4XTzzPdVZu1xkRtb17nhA20SUg9gwCOPD6uLU4ml1aOPHBdiMLKz66inI8txPrRK57G' \
                                 'n33m8lVp0WTOOgLV5MkCIpkgVHBl50EHcQFA5KfPet3FBLjpp2I1yThQe_n1Zc6GdnR0v_nqX0JhmmDMOvJ5rh' \
                                 'IHZ7B0hEtFy9rKUWOWfcug'
    os.environ['PLUGIN_COURSE'] = "def_course"

    update_url = os.environ['PLUGIN_API'] + os.environ['PLUGIN_COURSE'] + '/update'

    headers = {
            'Authorization': 'Bearer {}'.format(os.environ['PLUGIN_TOKEN'])
            }

    # Send a request to mooc-grader to update index.yaml
    r = requests.post(update_url, headers=headers, data={'status': 'success'})
    if r.status_code == 200:

        updated_index = r.json()['updated_index']

        with open(generated_dir + 'update.yaml', 'w', encoding='utf8') as update_yaml:
            yaml.dump(updated_index, update_yaml)

        aplus_json = aplus_json(course, updated_index)
        with open(generated_dir+"aplus.json", "w") as aplus_json_file:
            json.dump(aplus_json, aplus_json_file, indent=4, sort_keys=True)

    else:
        raise Exception('Fail to update index.yaml!')


