from py_api.routes.utility import UtilityRoutes

"""
    If you need to disable request verification for a particular endpoint,
    you can do that in packages/py-api/py_api/middleware/auth.py
    by adding them to the BYPASSED_ENDPOINTS dictionary.
"""


class Routes:
    @staticmethod
    def bind(app):
        UtilityRoutes.bind(app)
