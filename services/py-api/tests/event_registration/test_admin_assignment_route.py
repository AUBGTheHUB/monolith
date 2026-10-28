from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from src.server.routes.registration_routes import register_registration_routes
from src.server.utility.role_checker import RoleChecker


PARTICIPANT_ID = "507f1f77bcf86cd799439011"
TEAM_ID = "507f191e810c19729de860ea"

PAYLOAD = {
    "participant_id": PARTICIPANT_ID,
    "team_code": "ABC123",
    "assigned_role": "Designer",
}


class FakeRegistrationHandlers:

    def __init__(self):
        self.assignment_calls = 0

    async def assign_solo_handler(self, request, background_tasks):
        self.assignment_calls += 1

        return {
            "participant_id": request.participant_id,
            "team_id": TEAM_ID,
            "assigned_role": request.assigned_role,
        }


def create_test_app():
    app = FastAPI()
    handlers = FakeRegistrationHandlers()

    app.include_router(register_registration_routes(handlers))

    route = next(
        route for route in app.routes if isinstance(route, APIRoute) and route.path == "/registration/admin/assign-solo"
    )

    checker = next(
        dependency.call for dependency in route.dependant.dependencies if isinstance(dependency.call, RoleChecker)
    )

    return app, handlers, checker


def test_assignment_is_blocked_when_authorization_rejects():
    app, handlers, checker = create_test_app()

    async def deny_access():
        raise HTTPException(status_code=403, detail="Forbidden")

    app.dependency_overrides[checker] = deny_access

    with TestClient(app) as client:
        response = client.post(
            "/registration/admin/assign-solo",
            json=PAYLOAD,
        )

    assert response.status_code == 403
    assert handlers.assignment_calls == 0


def test_assignment_reaches_handler_when_authorized():
    app, handlers, checker = create_test_app()

    async def allow_access():
        return None

    app.dependency_overrides[checker] = allow_access

    with TestClient(app) as client:
        response = client.post(
            "/registration/admin/assign-solo",
            json=PAYLOAD,
        )

    assert response.status_code == 200
    assert response.json() == {
        "participant_id": PARTICIPANT_ID,
        "team_id": TEAM_ID,
        "assigned_role": "Designer",
    }
    assert handlers.assignment_calls == 1
