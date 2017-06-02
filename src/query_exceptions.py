# query_exceptions.py
# General API exception handling

def valid_exceptions():
    return exceptions.keys()

def raise_exception(code):
    if code not in valid_exceptions():
        raise Exception("Tried to raise exception, but no Error %d exists" % code)
    raise exceptions[code]()

class q400Exception(Exception):
    """Bad request exception"""
    def __init__(self):
        Exception.__init__(self, "Bad request. Try again with something else.")

class q401Exception(Exception):
    """Unauthorized exception"""
    def __init__(self):
        Exception.__init__(self, "Unauthorized request. Please get proper permissions first.")

class q404Exception(Exception):
    """Data not found exception"""
    def __init__(self):
        Exception.__init__(self, "Data not found. Try a different request.")

class q429Exception(Exception):
    """Rate limit exceeded exception"""
    def __init__(self):
        Exception.__init__(self, "Rate limit exceeded. Try again in 10 seconds//1 minute.")

class q500Exception(Exception):
    """Internal server error exception"""
    def __init__(self):
        Exception.__init__(self, "Internal server error. Try again in a moment.")

class q503Exception(Exception):
    """Service unavailable exception"""
    def __init__(self):
        Exception.__init__(self, "Service unavailable. Try again later.")

exceptions = {
    400: q400Exception,
    401: q401Exception,
    404: q404Exception,
    429: q429Exception,
    500: q500Exception,
    503: q503Exception
}
