# How to write unit tests

### 1. Read about `pytest` [here](https://docs.pytest.org/en/stable/how-to/index.html)

---

### 2. Use `pytest` Fixtures for Setup and Repeated Code
`pytest` fixtures are a powerful tool for handling setup tasks or reusable code across multiple tests. When you have common dependencies, objects, or configurations required by multiple tests, fixtures can simplify your test suite by making these elements reusable.

- **Define Common Fixtures**: Place shared fixtures in a [conftest.py](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files) file so they’re accessible to all tests within the directory. This keeps fixtures organized and ensures they’re automatically available without needing to import them into individual test files.

To learn more about `pytest` fixtures, check the [official documentation](https://docs.pytest.org/en/stable/explanation/fixtures.html).

---

### 3. Check what it Dependency Injection [here](https://www.youtube.com/watch?v=J1f5b4vcxCQ)

### 4. Using Mocks for Injected Dependencies

We use mocking to replace injected dependencies with fake ones, especially when our code is designed with "composition over inheritance." This approach makes it easier to substitute real dependencies with mocks in unit tests.

1. **`Mock`**: Use [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock) for simple objects that don’t require magic methods (e.g., objects with basic attributes or methods but no special behaviors). If you are mocking classes use (spec=ClassName). Read more about it in the official docs.
2. **`MagicMock`**: Use [MagicMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock) for more complex objects that have magic methods, like `__call__`, `__getitem__`, etc. This mock automatically provides these special methods, making it suitable for more intricate objects.
3. **`AsyncMock`**: Use [AsyncMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock) when mocking `async` functions. `AsyncMock`.

Read more about [return_value](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value) which is used to mock the return values of functions and [side_effect](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect) which is often used for mocking raising an Exception.

#### Example: How to use Mock and AsyncMock

Here’s a class that uses dependency injection (we inject a HackathonService instance):
```python
class ParticipantRegistrationService:
    """Service layer responsible for handling the business logic when registering a participant"""

    def __init__(self, hackathon_service: HackathonService) -> None:
        self._hackathon_service = hackathon_service

    async def register_admin_participant(self, input_data: ParticipantRequestBody) -> Result[
        Tuple[Participant, Team],
        DuplicateEmailError | DuplicateTeamNameError | HackathonCapacityExceededError | Exception,
    ]:
        # Capacity Check 2
        has_capacity = await self._hackathon_service.check_capacity_register_admin_participant_case()
        if not has_capacity:
            return Err(HackathonCapacityExceededError())

        # Proceed with registration if there is capacity
        return await self._hackathon_service.create_participant_and_team_in_transaction(input_data)

```
As this class is written with Dependency Injection in mind we could use a Mock object to test it.


1. First we crete the mock. It could be a `pytest fixture` placed inside the `conftest.py` in order for it to be reused
across tests. Here we create a Mock specified to the `HackathonService`, and we use `AsyncMock` to replace the actual versions of its `async` methods with fake ones.
This is done firstly to isolate behaviour of a method when testing it, secondly in this case the methods of this class make real DB connections which we don't want to happen during unit testing. (Real connections are made in integration tests).
And lastly we could control the behaviour of these methods during testing, to adhere to our particular needs.

```python
@pytest.fixture
def hackathon_service_mock() -> Mock:
    hackathon_service = Mock(spec=HackathonService)

    hackathon_service.create_participant_and_team_in_transaction = AsyncMock()
    hackathon_service.check_capacity_register_admin_participant_case = AsyncMock()

    return hackathon_service
```

2. Now we write a test case for a given behaviour:

Here we assume the creation of `ParticipantRegistrationService` would happen often, that's why we create a fixture.
`mock_input_data` is a fixture located in `conftest.py`

```python
@pytest.fixture
def p_reg_service(hackathon_service_mock: Mock) -> ParticipantRegistrationService:
    return ParticipantRegistrationService(hackathon_service_mock)

@pytest.mark.asyncio
async def test_register_admin_participant_duplicate_team_name_error(
    p_reg_service: ParticipantRegistrationService,
    hackathon_service_mock: Mock,
    mock_input_data: ParticipantRequestBody,
) -> None:
    # Mock not full hackathon
    hackathon_service_mock.check_capacity_register_admin_participant_case = AsyncMock(return_value=True)

    # Mock `create_participant_and_team_in_transaction` to return an `Err` for duplicate team name
    hackathon_service_mock.create_participant_and_team_in_transaction.return_value = Err(
        DuplicateTeamNameError(mock_input_data.team_name)
    )

    # Call the function under test
    result = await p_reg_service.register_admin_participant(mock_input_data)

    # Check that the result is an `Err` with `DuplicateTeamNameError`
    assert isinstance(result, Err)
    assert isinstance(result.err_value, DuplicateTeamNameError)
    assert str(result.err_value) == mock_input_data.team_name
```
---

### 5. Using [with patch](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch) for Functions from External Modules or Libraries

Use `with patch` when the function you’re testing calls functions, classes, or objects from external modules or libraries that are not injected as dependencies. Since you don’t have direct access to these external modules within the function’s parameters, `patch` allows you to replace them temporarily for testing.

#### Example: Mocking `asyncio.sleep` with `patch`

In the example below, `retry_logic` uses `asyncio.sleep` to introduce a delay between retries. We don’t directly inject `sleep` as a dependency, so we use `patch` to replace it temporarily within the `my_module` namespace.

```python
# my_module.py
import asyncio

async def retry_logic(operation, retries=3):
    for _ in range(retries):
        try:
            return await operation()
        except Exception:
            await asyncio.sleep(1)  # Delay before retrying
    raise Exception("Operation failed after retries")

```
#### Test with `patch`

To test `retry_logic` without real delays, we use `patch` to mock `asyncio.sleep` in the `my_module` namespace:
```python
# test_my_module.py
import pytest
from unittest.mock import AsyncMock, patch
from my_module import retry_logic

@pytest.mark.asyncio
async def test_retry_logic():
    mock_operation = AsyncMock(side_effect=Exception("Failure"))

    # Patch `asyncio.sleep` in `my_module` to avoid real delays
    with patch("my_module.asyncio.sleep", new=AsyncMock):
        with pytest.raises(Exception, match="Operation failed after retries"):
            await retry_logic(mock_operation, retries=3)

    # Check that `mock_operation` was called three times due to retries
    assert mock_operation.call_count == 3

```
#### Explanation of `patch` and `new`

- **`new=AsyncMock`**: Directly assigns a specific mock object as the replacement. With `new`, you are giving `patch` an actual instance to use in place of the target.
- **Scope of `with patch`**: The `patch` replacement only applies within the `with` block. Outside of it, `asyncio.sleep` behaves normally.

In short, use `with patch` for cases where the functions or classes you want to mock are part of an external module or library, and you don’t have direct access to them as injected dependencies. This technique is particularly helpful when testing code that’s not designed with Dependency Injection in mind.

Read more about where to patch [here](https://docs.python.org/3/library/unittest.mock.html#where-to-patch)
