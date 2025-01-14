import pydantic


def to_lower_camel_case(snake_str: str) -> str:
    # We capitalize the first letter of each component except the first one
    camel_string = "".join(x.capitalize() for x in snake_str.lower().split("_"))
    return snake_str[0].lower() + camel_string[1:]


class CamelCaseDTO(pydantic.BaseModel):
    """
    This is a base schema intended for all API facing schemas
    to have the came casing functionality.

    when you create your schema extending from this one you API
    will expect both request and response to
    have camelCasing.
    """
    
    if pydantic.__version__.startswith("2"):
        model_config = pydantic.ConfigDict(
            populate_by_name=True, 
            alias_generator=to_lower_camel_case
        )
    else:

        class Config:
            alias_generator = to_lower_camel_case
            allow_population_by_field_name = True

