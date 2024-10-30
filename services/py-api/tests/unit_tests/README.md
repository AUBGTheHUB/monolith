# How to write unit tests

### 1. Read about `pytest` [here](https://docs.pytest.org/en/stable/how-to/index.html)

---

### 2. Use `pytest` Fixtures for Setup and Repeated Code
`pytest` fixtures are a powerful tool for handling setup tasks or reusable code across multiple tests. When you have common dependencies, objects, or configurations required by multiple tests, fixtures can simplify your test suite by making these elements reusable.

- **Define Common Fixtures**: Place shared fixtures in a `conftest.py` file so they’re accessible to all tests within the directory. This keeps fixtures organized and ensures they’re automatically available without needing to import them into individual test files.

To learn more about `pytest` fixtures, check the [official documentation](https://docs.pytest.org/en/stable/explanation/fixtures.html).

---

### 3. Using Mocks for Injected Dependencies

We use mocking to replace injected dependencies with fake ones, especially when our code is designed with "composition over inheritance." This approach makes it easier to substitute real dependencies with mocks in unit tests.

1. **`Mock`**: Use `Mock` for simple objects that don’t require magic methods (e.g., objects with basic attributes or methods but no special behaviors).
2. **`MagicMock`**: Use `MagicMock` for more complex objects that have magic methods, like `__call__`, `__getitem__`, etc. This mock automatically provides these special methods, making it suitable for more intricate objects.
3. **`AsyncMock`**: Use `AsyncMock` for objects with `async` methods, or when mocking `async` methods specifically. `AsyncMock` allows you to use `await` and to control behaviors with `return_value` or `side_effect`. `side_effect` is often used to simulate errors by raising an `Exception`.

#### Example: Using Dependency Injection with `AsyncMock`

Here’s a class that uses dependency injection, and a test that uses `AsyncMock` for testing without the actual database dependency.
```python
# my_processor.py
class DataProcessor:
    # `db_client` is injected as a dependency
    def __init__(self, db_client):
        self.db_client = db_client

    async def process_data(self, data):
        await self.db_client.save(data)
        return "Data processed"

```
#### Test with `AsyncMock`
```python
# test_my_processor.py
import pytest
from unittest.mock import AsyncMock
from my_processor import DataProcessor

@pytest.mark.asyncio
async def test_process_data():
    # Create an AsyncMock for `db_client`
    mock_db_client = AsyncMock()
    processor = DataProcessor(mock_db_client)

    # Call the method under test
    result = await processor.process_data("sample data")

    # Assertions
    # Check db_client.save was called with the right data
    mock_db_client.save.assert_awaited_once_with("sample data")
    assert result == "Data processed"

```
This approach allows us to control the behavior of `db_client` without the need for an actual database, ensuring our test is fast and isolated.

---

### 4. Using `with patch` for Functions from External Modules or Libraries

Use `with patch` when the function you’re testing calls functions, classes, or objects from external modules or libraries that are not injected as dependencies. Since you don’t have direct access to these external functions within the function’s parameters, `patch` allows you to replace them temporarily for testing.

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
    with patch("my_module.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(Exception, match="Operation failed after retries"):
            await retry_logic(mock_operation, retries=3)

    # Check that `mock_operation` was called three times due to retries
    assert mock_operation.call_count == 3

```
#### Explanation of `patch` and `new_callable`

- **`new_callable=AsyncMock`**: `patch` creates a mock of the specified type (`AsyncMock` in this case) for the patched function. This ensures `asyncio.sleep` behaves as an async function without introducing real delays.
- **Scope of `with patch`**: The `patch` replacement only applies within the `with` block. Outside of it, `asyncio.sleep` behaves normally.

In short, use `with patch` for cases where the functions or classes you want to mock are part of an external module or library, and you don’t have direct access to them as injected dependencies. This technique is particularly helpful when testing code that’s not designed with Dependency Injection in mind.
