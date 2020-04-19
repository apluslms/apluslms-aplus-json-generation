import os

from apluslms_yamlidator.validator import Validator

# Set up validator
APP_PATH = '/app'
validator = Validator(dirs=[os.path.join(APP_PATH, 'schemas')])
_v, ref = validator.get_version('index', 1)
schema = validator.get_schema(ref)
# with open("schema.json", "w") as schema_json:
#     json.dump(schema, schema_json, indent=4, sort_keys=True)

APLUS_JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aplus_json')

# COURSE_DIR = "/u/71/qinq1/unix/Desktop/my_new_course"
COURSE_DIR = os.getcwd()
YAML_DIR = "_build/yaml"
COURSE_YAML_DIR = os.path.join(COURSE_DIR, YAML_DIR)
INDEX_YAML = "index.yaml"
