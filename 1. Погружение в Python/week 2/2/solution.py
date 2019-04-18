import json
import functools

def to_json(func):
    @functools.wraps(func) # Это поможет нам при откладке
    def wrapped(*args, **kwargs):
        return json.dumps(func(*args, *kwargs))
    return wrapped

