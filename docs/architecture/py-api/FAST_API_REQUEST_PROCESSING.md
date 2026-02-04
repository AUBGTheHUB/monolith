## How a request is processed by FastAPI


1. A request comes to the uvicorn server, which under the hood is just a giant coroutine that gets executed by a running event [EventLoop](https://docs.python.org/3.13/library/asyncio-eventloop.html#asyncio-event-loop) via the standard [asyncio.run](https://docs.python.org/3.13/library/asyncio-runner.html#asyncio.run) [here](https://github.com/Kludex/uvicorn/blob/8ae0bcbecb0a655789abf0c2dd4200848fc68a30/uvicorn/server.py#L67)

What is an HTTP Request under the hood? As you know, it's just a stream of data sent over the established TCP socket between the Client and the Server.

Well, this is important to note, as during the startup phase of the server, it establishes such a TCP socket connection [here](https://github.com/Kludex/uvicorn/blob/8ae0bcbecb0a655789abf0c2dd4200848fc68a30/uvicorn/server.py#L142). The listening on this TCP socket happens via the [tooling provided by the Python standard library.](https://docs.python.org/3.13/library/asyncio-eventloop.html#loop-create-server), which is basically a TCP server that uses some protocol. TCP is the [transport layer](https://docs.python.org/3.13/library/asyncio-protocol.html#asyncio-transport), but on top of it we have protocols. In our case, the protocol is HTTP 1.1 ([H11Protocol](https://github.com/Kludex/uvicorn/blob/main/uvicorn/protocols/http/h11_impl.py)).

When data comes over the TCP connection, under the hood, the TCP server calls the [data_received](https://github.com/Kludex/uvicorn/blob/8ae0bcbecb0a655789abf0c2dd4200848fc68a30/uvicorn/protocols/http/h11_impl.py#L168) function of the H11Protocol.

2. The H11Protocol calls our [FastAPI ASGI application](https://github.com/AUBGTheHUB/monolith/blob/10b4339e01db500c1a3c0133c2f644c6e3b3d569/services/py-api/src/app_entrypoint.py#L15C1-L15C19) [here](https://github.com/Kludex/uvicorn/blob/8ae0bcbecb0a655789abf0c2dd4200848fc68a30/uvicorn/protocols/http/h11_impl.py#L250), which, as we see, gets called by the uvicorn server for each TCP connection opened, just exaclty as per the ASGI spec [here](https://asgi.readthedocs.io/en/latest/specs/main.html#overview)

3. This executes the `__call__` of the [FastAPI ASGI app](https://github.com/fastapi/fastapi/blob/6fae64ff49e8328048872714652a4dfa15406e41/fastapi/applications.py#L1131), which in turn calls the `__call__` [of the Starlette](https://github.com/Kludex/starlette/blob/49d4de92867cb38a781069701ad57cecab4a1a36/starlette/applications.py#L103), as FastAPI is a wrapper around Starlette.
This firstly executes all middlewares in the middleware chain, and then calls the [main Router](https://github.com/Kludex/starlette/blob/49d4de92867cb38a781069701ad57cecab4a1a36/starlette/applications.py#L91C9-L91C26). The Router is responsible for matching the URL patterns and calling the respective handler function, which we have [registered](https://github.com/AUBGTheHUB/monolith/blob/10b4339e01db500c1a3c0133c2f644c6e3b3d569/services/py-api/src/server/routes/routes.py#L14). As we are registering FastAPI routers, and not Starlette, there is a bit of diff in how the router handles the request.

4. Before our handler functions get called, FastAPI first [executes the dependencies attached to these handler funcs](https://github.com/fastapi/fastapi/blob/6fae64ff49e8328048872714652a4dfa15406e41/fastapi/routing.py#L381), before actually running the actual handler func. And the result from these executed dependencies then gets [passed as values to the actual handler function.](https://github.com/fastapi/fastapi/blob/6fae64ff49e8328048872714652a4dfa15406e41/fastapi/routing.py#L391C13-L395C14)

## Notes

Some of our route dependencies, such as [is_authorized](https://github.com/AUBGTheHUB/monolith/blob/656f5677b6a77471b150dd2a543a58131ecc7bba/services/py-api/src/server/routes/route_dependencies.py#L29), should not really return a `Response` object, as we want an early break of the control flow, before we even get to our handler function, and this could be achieved via raising an HTTPException, which will be caught by the [Starlette Middleware.](https://github.com/Kludex/starlette/blob/49d4de92867cb38a781069701ad57cecab4a1a36/starlette/_exception_handler.py#L23)

If you are interested in diving deeper, and you want to know how the EventLoop works and executes the operations required for handling the request you can check out [this discussion.](https://github.com/AUBGTheHUB/monolith/discussions/774)
