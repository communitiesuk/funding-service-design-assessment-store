import json
from jsonschema import validate
from mapping_schema import top_level_assessment_mapping_schema as schema

with open("config/mappings/mapping.json", "r") as mapping_file:
    mapping = json.load(mapping_file)

validate(instance=mapping, schema=schema)
print("Mapping conforms with schema.")
