from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    """Custom validator for ObjectId (convert to/from string)"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        """
        This method is responsible for generating the core schema for `ObjectId`.
        """
        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """
        Modify the schema to reflect ObjectId as a string in the JSON schema.
        """
        schema = handler(core_schema)
        schema.update(type="string")
    #     return schema
