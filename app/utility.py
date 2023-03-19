import json
from pydantic import BaseModel, error_wrappers

def data_or_error_validation_schema(raw_data: dict, SchemaModel:BaseModel):
    data = {}
    errors = []
    error_str = None
    try:
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, errors