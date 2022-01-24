import uvicorn
from fastapi import Request
from fastapi.param_functions import Query
from fastapi import FastAPI
from migrations import migrate
from crud import (
    create_user,
    update_user,
    get_user,
    get_users,
    delete_user,
    create_poll,
    update_poll,
    get_poll,
    get_polls,
    delete_poll,
    create_vote,
    update_vote,
    get_vote,
    get_votes_poll,
    delete_vote,
)

ovs = FastAPI()
migrate()


@ovs.post("/login")
async def root(userhash: str = Query(...)):

    return {"userhash": userhash}

    

if __name__ == "__main__":
    uvicorn.run(ovs, host="0.0.0.0", port=8000)
