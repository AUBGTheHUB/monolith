from fastapi.routing import APIRoute

from src.app_factory import create_app


def test_registration_routes_are_connected():
    app = create_app()

    registered_routes = {
        (route.path, method) for route in app.routes if isinstance(route, APIRoute) for method in route.methods
    }

    expected_routes = {
        ("/registration/team/admin", "POST"),
        ("/registration/team/member", "POST"),
        ("/registration/solo", "POST"),
    }

    assert expected_routes.issubset(registered_routes)


def test_backfill_route_is_not_public():
    app = create_app()

    registered_paths = {route.path for route in app.routes if isinstance(route, APIRoute)}

    assert "/registration/team/backfill" not in registered_paths
