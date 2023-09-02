
def handle_exception(func):  # type: ignore
    def wrapper(*arg, **kwargs):  # type: ignore
        request = arg[0]
        try:
            response = func(*arg, **kwargs)
            return response
        except Exception as e:
            e.handle_body = request.body  # type: ignore
            raise e

    return wrapper
