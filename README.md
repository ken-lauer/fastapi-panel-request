# fastapi-panel-request

A quick example of how to access the `Request` object while using FastAPI's
[Panel](https://panel.holoviz.org/) integration, which does not currently
support dependency injection.

## Setup

In order to add authentication and add user information in the request header,
first configure an Nginx reverse proxy.
[oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) is recommended.

Double-check that the nginx `location` for your pages should include these lines:

```
    proxy_set_header X-User  $user;
    proxy_set_header X-Email $email;
```

### Running it locally

1. `mamba env create -f env.yaml`
2. `make dev`

### Running it in a container

1. `make build run`
