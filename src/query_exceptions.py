# query_exceptions.py
# General API exception handling

def valid_exceptions():
    return exceptions.keys()

def raise_exception(code, query, response):
    if code not in valid_exceptions():
        raise Exception("Tried to raise exception, but no Error %d exists" % code)
    raise exceptions[code](query, response)

def exception_message(message, query, response):
    return "Error: %s\nQuery:\n\t%s\nResponse:\n\t%s" % (message, query, response)

class q400Exception(Exception):
    """Bad request exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Bad request. Try again with something else.", query, response))

class q401Exception(Exception):
    """Unauthorized exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Unauthorized request. Please get proper permissions first.", query, response))

class q404Exception(Exception):
    """Data not found exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Data not found. Try a different request.", query, response))

class q429Exception(Exception):
    """Rate limit exceeded exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Rate limit exceeded. Try again in 10 seconds//1 minute.", query, response))

class q500Exception(Exception):
    """Internal server error exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Internal server error. Try again in a moment.", query, response))

class q503Exception(Exception):
    """Service unavailable exception"""
    def __init__(self, query, response):
        Exception.__init__(self, exception_message("Service unavailable. Try again later.", query, response))

exceptions = {
    400: q400Exception,
    401: q401Exception,
    404: q404Exception,
    429: q429Exception,
    500: q500Exception,
    503: q503Exception
}
