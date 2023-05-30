import asyncio

import uvicorn
from fastapi import FastAPI

from app.api.handlers import router
from app.api.tasks import rocketry

app = FastAPI(title="WelbeX")


app.include_router(router)


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run scheduler and the API"
    server = Server(config=uvicorn.Config(app=app, host="0.0.0.0", port=8000))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(rocketry.serve())

    await asyncio.wait([sched, api])


if __name__ == "__main__":
    asyncio.run(main())
