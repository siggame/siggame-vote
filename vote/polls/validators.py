from django.core.exceptions import ValidationError
from jsonschema import validate
from jsonschema import ValidationError as JSONValidationError
import json


ballotschema = {
    "type": "array",
    "items": {
        "type": "string"
    },
    "minItems": 1,
    "uniqueItems": True
}


def validate_ballot(value):
    try:
        obj = json.loads(value)
        validate(obj, ballotschema)
    except ValueError:
        raise ValidationError("Could not decode JSON from data")
    except JSONValidationError:
        raise ValidationError("Bad data. Should be an array of strings.")
