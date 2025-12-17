import json
from jsonschema import validate, ValidationError


class OutputValidator:
    def __init__(self, schema: dict):
        self.schema = schema

    def validate(self, output: str):
        try:
            parsed = json.loads(output)
            validate(instance=parsed, schema=self.schema)
            return True, parsed
        except (json.JSONDecodeError, ValidationError) as e:
            return False, str(e)
