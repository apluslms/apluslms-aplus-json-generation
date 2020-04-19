import os
import json
import requests

from config import validator, COURSE_DIR, COURSE_YAML_DIR, INDEX_YAML
from course import Course
from parser import yaml
from utils import aplus_json

# os.environ['PLUGIN_API'] = 'http://0.0.0.0:8080/api/v1/'
# os.environ['PLUGIN_TOKEN'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkZWZfY291cnNlIiwiaWF0IjoxNTYyODI4MzA0L' \
#                              'CJpc3MiOiJzaGVwaGVyZCJ9.MUkoD27P6qZKKMM5juL0e0pZl8OVH6S17N_ZFzC7D0cwOgbcDaAO3S1BauXzhQ' \
#                              'OneChPs1KEzUxI2dVF-Od_gpN8_IJEnQnk25XmZYecfdoJ5ST-6YonVmUMzKP7UAcvzCFye7mkX7zJ1ADYtda5' \
#                              '7IUdyaLSPOWnFBSHX5B4XTzzPdVZu1xkRtb17nhA20SUg9gwCOPD6uLU4ml1aOPHBdiMLKz66inI8txPrRK57G' \
#                              'n33m8lVp0WTOOgLV5MkCIpkgVHBl50EHcQFA5KfPet3FBLjpp2I1yThQe_n1Zc6GdnR0v_nqX0JhmmDMOvJ5rh' \
#                              'IHZ7B0hEtFy9rKUWOWfcug'
# os.environ['PLUGIN_COURSE'] = "def_course"

if __name__ == "__main__":

    # Load and parse course index.yaml
    course = Course(COURSE_YAML_DIR)
    course.load(INDEX_YAML)
    course_data = course.get_data()
    # with open("course.json", "w") as course_json:
    #     json.dump(course_data, course_json, indent=4, sort_keys=True)

    # Validate index.yaml
    if not validator.validate(course_data, 'index', major=1):
        raise ValueError('Invalid index.yaml')

    update_url = os.environ['PLUGIN_API'] + os.environ['PLUGIN_COURSE'] + '/update-index-file'
    headers = {
            'Authorization': 'Bearer {}'.format(os.environ['PLUGIN_TOKEN'])
            }
    # Send a request to mooc-grader to update index.yaml
    r = requests.post(update_url, headers=headers)
    if r.status_code != 200:
        raise Exception('Fail to update index.yaml: ', r.text)

    updated_index = r.json()['updated_index']
    with open(os.path.join(COURSE_YAML_DIR, 'updated_index.yaml'), 'w', encoding='utf8') as updated_yaml:
        yaml.dump(updated_index, updated_yaml)

    aplus_json = aplus_json(course, updated_index)
    aplus_json_file = os.path.join(COURSE_DIR,
                                   os.environ['PLUGIN_COURSE'] + "_aplus.json")
    with open(aplus_json_file, "w") as f:
        json.dump(aplus_json, f, indent=4, sort_keys=True)

    print("Aplus json file is generated: {}!".format(os.path.relpath(aplus_json_file, start=COURSE_DIR)))



