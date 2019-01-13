def validate_requirements(*required_fields):
    """
    Check if each string in required_fields has a key in function parameters dict

    Args:
        *required_fields: A tuple of field names to check in function parameters

    """
    def decorator(func):
        def wrapper(self, params):
            obtained_fields = list(params.keys())
            for required_field in required_fields:
                if required_field not in obtained_fields:
                    # TODO
                    print('Obrigatorio!')
            return func(self, params)
        return wrapper
    return decorator
