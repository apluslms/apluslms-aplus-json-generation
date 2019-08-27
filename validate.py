import logging
from apluslms_yamlidator.validator import Validator
from apluslms_yamlidator import schemas
from apluslms_yamlidator.utils.yaml import rt_dump
import json
from utils import *


logger = logging.getLogger(__name__)


BASE_URL = 'http://localhost:8080/'
KEY = 'static/'
STATIC_URL = BASE_URL + KEY

course_key = 'default'
generated_dir = 'generated/'

# Set up validator
validator = Validator(dirs=['schemas'])
_v, ref = validator.get_version('index', 1)
schema = validator.get_schema(ref)
with open(generated_dir+"schema.json", "w") as schema_json:
    json.dump(schema, schema_json, indent=4, sort_keys=True)


# Load and parse course index.yaml
_, data_loader = schemas.get_file_loader('index_instance/index.yaml')
course_data = data_loader()
# course = rt_load(open('index_instance/index.yaml','rb').read())
with open(generated_dir+"course.json", "w") as course_json:
    json.dump(course_data, course_json, indent=4, sort_keys=True)


# Validate index.yaml
# if not validator.validate(course_data, 'index', major=1):
#     raise ValueError('Invalid index.yaml')

# Update urls in index.yaml
update_index_yaml(STATIC_URL, course_key, course_data)

# Save the updated index.yaml
with open(generated_dir+'update.yaml', 'w', encoding='utf8') as update_yaml:
    rt_dump(course_data, update_yaml, allow_unicode=True)
_, data_loader = schemas.get_file_loader('update.yaml')
update = data_loader()
with open(generated_dir+"update.json", "w") as update_json:
    json.dump(update, update_json, indent=4, sort_keys=True)


# # Send to mooc-grader
# request_url = 'http://0.0.0.0:8080/api/v1/validate/'
# request = requests.post(request_url, data={'status': 'success'})


