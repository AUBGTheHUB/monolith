## How we do Dependency Injection
Across our codebase we use FastAPI's built in [Dependency Injection system](https://fastapi.tiangolo.com/tutorial/dependencies/).
FastAPI automatically injects dependencies into consumers, when they are passed as params using ``fastapi.Depends``, meaning:

```python
def some_instance_provider() -> SomeInstance:
    return SomeInstance()

# foo accepts an instance which will be automatically injected by FastAPI
def foo(dep: SomeInstance = Depends(some_instance_provider) -> Bar:
   ...
```

Under the `Depends` calls the passed callable (instance_provider) and adds this dependency to the Dependency graph.

## What is our Dependency graph
The routes are the entrypoint of incoming requests. For separation of concerns these requests are passed to HTTP
handlers, which are injected into the routes via FastAPI. After that, FastAPI traverses the Dependency graph, resolving
dependencies along the way. (Handlers have dependencies and these dependencies have their own dependencies
and so on...)

A graphical representation of this graph looks something like this:
```
                          Repositories -> DbManagers -> DbClients
                         /
Routes -> Handlers -> Services -> OtherServices -> OtherComponents
                         \
                          MailServices ->  MailClients
```

## How to add a new dependency and inject it into its consumers

1. Create a class
```python
class DbClient:
    ...
```

2. Create a provider
```python
# Every new dependency (class) show come with a so-called provider. This is a function which when called provides an
# instance of this class
def db_client_provider() -> DbClient:
    return DbClient()

# Create a FastApi Dependency, which when called will automatically inject the instance into the consumer
DbClientDep = Annotated[DbClient, Depends(db_client_provider)]
```

3. Inject the dependency
```python
# We assume the consumer is another class (another dependency), which should have its own provider as mentioned above
class Consumer:
    def __init__(self, client: DbClient):
        ...

# As the Consumer class expects as dependency a DbClient instance we should tell FastAPI to automatically inject it.
# We could do that by using the already declared DbClientDep, which should be passed to the consumer_provider
# This is done so that when FastAPI traverses the Dependency graph it could resolve the Consumer dependency along with
# it's sub-dependencies (in this case DbClient)
def consumer_provider(client: DbClientDep) -> Consumer:
    return Consumer(client=client)

# Create a FastApi Dependency, so that the Consumer could be passed to other consumers downstream
ConsumerDep = Annotated[Consumer, Depends(consumer_provider)]
```
