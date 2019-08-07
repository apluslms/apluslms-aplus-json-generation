from apluslms_yamlidator import schemas, document, validator
import json

val = validator.Validator(dirs=['schemas'])

_v, ref = val.get_version('index', 1)
schema = val.get_schema(ref)

with open("schema.json", "w") as schema_json:
    json.dump(schema, schema_json, indent=4, sort_keys=True)

vali = validator._validator_for(schema)
vali.check_schema(schema)

# val.validate(data, 'index', major=1)

# _, data_loader = schemas.get_file_loader('index_instance/index.yaml')
# data = data_loader()

