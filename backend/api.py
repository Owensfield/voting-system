import uvicorn
from fastapi import Request
from pydantic import BaseModel
from fastapi.param_functions import Query
from fastapi import FastAPI
from migrations import migrate
from crud import (
    create_user,
    get_user,
    get_users,
    delete_user,
    create_poll,
    get_poll,
    get_polls,
    delete_poll,
    create_vote,
    get_vote,
    get_vote_poll,
)
from models import CreateUserData, CreateVoteData, CreatePollData, CreateVoteApprovalData

ovs = FastAPI()
migrate()

@ovs.post("/user")
async def ovs_api_create_user(
    data: CreateUserData):
    return await create_user(data)

@ovs.get("/user")
async def ovs_api_get_user(passhash: str) -> CreateUserData:
    return await get_user(passhash)

@ovs.get("/users")
async def ovs_api_get_users():
    return await get_users()

@ovs.delete("/user")
async def ovs_api_delete_user(passhash: str) -> None:
    return await delete_user(passhash)

### Polls

@ovs.post("/poll")
async def ovs_api_create_poll(data: CreatePollData):
    return await create_poll(data)

@ovs.get("/poll")
async def ovs_api_get_poll(poll_id: str):
    return await get_poll(poll_id)

@ovs.get("/polls")
async def ovs_api_get_polls():
    return await get_polls()

# Needs signture of person who created poll
@ovs.delete("/poll")
async def ovs_api_delete_poll(signature: str):
    return await delete_poll()

### Approvals

@ovs.post("/approval")
async def ovs_api_create_approval(data: CreateVoteApprovalData):
    return await create_approval(data)

@ovs.post("/approval")
async def ovs_api_check_approval(poll_id: str) -> CreateVoteApprovalData:
    return await check_approval(poll_id)


### Votes

@ovs.post("/vote")
async def ovs_api_create_vote(data: CreateVoteData):
    return await create_vote(data)

async def get_vote(vote_id: str) -> CreateVoteData:
    return await get_vote(vote_id)

async def get_vote_poll(poll_id: str) -> CreateVoteData:
    return await get_vote_poll(poll_id)

async def check_vote(user_id: str) -> CreateVoteData:
    return await check_vote(vote_id)


if __name__ == "__main__":
    uvicorn.run(ovs, host="0.0.0.0", port=8000)
