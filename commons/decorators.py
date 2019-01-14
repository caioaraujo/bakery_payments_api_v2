from django.utils.translation import ugettext
from rest_framework.exceptions import NotAcceptable


def validate_requirements(*required_fields):
    """
    Check if each string in required_fields has a key in function parameters dict

    Args:
        *required_fields: A tuple of field names to check in function parameters

    """
    def decorator(func):
        def wrapper(self, params):
            message = ugettext('Required field')
            invalid_data = dict()

            obtained_fields = list(params.keys())
            for required_field in required_fields:
                if required_field not in obtained_fields:
                    invalid_data[required_field] = message

            if invalid_data:
                raise NotAcceptable(detail=invalid_data)
            return func(self, params)
        return wrapper
    return decorator
