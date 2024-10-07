import contextvars
from typing import Callable

import panel as pn
import uvicorn
from fastapi import FastAPI, Request, Response
from panel.io.fastapi import add_applications

app = FastAPI()

request_ctx: contextvars.ContextVar[Request | None] = contextvars.ContextVar(
    "request_ctx", default=None
)


def home_panel():
    # We can't use FastAPI 'Depends' dependency injection in these functions.
    # So to get access to the Request itself, we need to use our contextvar.
    request: Request | None = request_ctx.get()
    assert request is not None

    # NOTE: this specific header key assumes an oauth2-proxy (or similar) is
    # configured externally and providing relevant headers.
    user_email = request.headers.get("x-email", "unknown")

    # Do some arbitrary gatekeeping based on user e-mail:
    if not user_email.endswith(".com"):
        return "No access"

    slider = pn.widgets.IntSlider(
        name="Slider",
        start=0,
        end=10,
        value=3,
    )

    root_path = request.scope["root_path"]
    return pn.layout.Column(
        f"Hello, {user_email}",
        slider.rx() * "⭐",
        # Use markdown syntax for links:
        f"[Panel 1 (markdown)]({root_path}/panel1)",
        # Or HTML:
        f'<a href="{root_path}/panel1">Panel 1 (html link)</a>',
        f'<a href="{root_path}/panel2">Panel 2</a>',
    )


def panel1():
    slider = pn.widgets.IntSlider(
        name="Panel 1 slider",
        start=0,
        end=10,
        value=3,
    )
    return slider.rx() * "(panel1)"


add_applications(
    {
        # Add your other Panel-related applications here:
        "/": home_panel,
        "/panel1": panel1,
        "/panel2": pn.Column("I am a Panel object!"),
    },
    app=app,
)

# Add normal FastAPI routes here:


@app.get("/json")
async def json_page(request: Request):
    return {
        "message": "Hello World",
        "your-email": request.headers.get("x-email", "unknown"),
    }


@app.middleware("http")
async def _add_request_context(request: Request, call_next: Callable) -> Response:
    try:
        request_ctx.set(request)
        return await call_next(request)
    finally:
        request_ctx.set(None)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
