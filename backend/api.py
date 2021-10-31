import uvicorn

from fastapi import FastAPI
from migrations import migrate

ovs = FastAPI()
migrate()


@ovs.get("/{userHash}")
async def root():

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(ovs, host="0.0.0.0", port=8000)
