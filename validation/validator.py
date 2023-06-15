import jsonschema


def validate(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError:
        return "error"
