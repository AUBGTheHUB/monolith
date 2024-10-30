# How to write integration tests

Integration tests check that various components of our application — such as routes, database interactions, and external
services—work together seamlessly.

### Writing Integration Tests for Endpoints

When testing endpoints, the goal is to verify that the endpoint responds correctly (e.g., status codes, JSON response).

Example:

```python
PING_ENDPOINT_URL = "/api/v3/ping"


@pytest.mark.asyncio
async def test_ping_endpoint(async_client: AsyncClient) -> None:
    resp = await async_client.get(PING_ENDPOINT_URL)
    assert resp.status_code == 200
    assert resp.json() == {"message": "pong"}
```

### Cleanup
When creating records in a database, integration tests should include cleanup steps to not clutter the database with
test records. This cleanup can often be handled by using delete endpoints for the relevant resource. For more
information on fixture finalization and teardown, refer to
the [official documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization).

To read more about the anatomy of a test click [here.](https://docs.pytest.org/en/stable/explanation/anatomy.html)
