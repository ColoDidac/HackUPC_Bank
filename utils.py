import re
from fastapi.encoders import jsonable_encoder


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def encode_json(data):
    return jsonable_encoder(data, exclude={'_data'})
