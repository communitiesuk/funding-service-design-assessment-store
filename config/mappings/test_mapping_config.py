import json
from jsonschema import validate
from assessment_mapping_schema import top_level_assessment_mapping_schema as schema
from assessment_mapping import cof_r2w2_assessment as mapping

validate(instance=mapping, schema=schema)
print("Mapping conforms with schema.")
