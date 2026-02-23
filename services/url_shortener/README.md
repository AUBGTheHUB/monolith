# URL SHORTENER
A url shortener which utilizes the currently deployed mongo clusters for storing created endpoints.

## What are endpoints in this case?
Endpoints are user chosen request endpoints which when accessed redirect the user to a specific url.
This specific url is chosen by the creator of the endpoint (probably in the ADMIN PANEL).

```json
{
    "endpoint": "example",
    "url": "https://somewhere.com"
}
```

In the example above, if you access our domain with an appended `/s/example` endpoint,
you will be redirected to `https://somewhere.com` (full url - `https://thehub-aubg.com/s/example`)

## Payload for creating an endpoint

```javascript
// Headers:
    Authorization: <token>  # BEARER from .env file

// Body:
    {
        "endpoint": "<endpoint>",
        "url": "<url>"
    }
```
