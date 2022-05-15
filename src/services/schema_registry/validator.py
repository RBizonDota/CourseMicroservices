import os
import jsonschema
import json

def validateMessage(domain, message):
    event_name = message.get('event_name')
    event_version = message.get('event_version')
    if not (event_name or event_version):
        raise jsonschema.ValidationError("Event name or version not specified")

    path = f'../schemas/{domain}/{event_name}/{event_version}.json'
    if not os.path.isfile(path):
        raise jsonschema.ValidationError("Schema for such configuration not specified")

    with open(path, 'r') as f:  
        schema = json.load(f)

    jsonschema.validate(instance=message, schema=schema)