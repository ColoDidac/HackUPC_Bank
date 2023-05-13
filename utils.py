import re


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def calculate_all(func):
    def wrap(*args, **kwargs):
        args[0].get_clear_transactions()
        args[0].get_upcoming_transactions()
        args[0].status_bank_review()
        args[0].calculate_avg()
        result = func(*args, **kwargs)
        return result
    return wrap
