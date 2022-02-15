import uvicorn
from fastapi import Request
from pydantic import BaseModel
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

class loginDetails(BaseModel):
    userhash: str

@ovs.post("/login")
async def root(data: loginDetails):
    get_user(data.userhash)
    return {"userhash": data.userhash}

@ovs.post("/user")
async def ovs_api_create_user(
    data: CreateUserData):
    return await create_user(data)

@ovs.get("/user")
async def ovs_api_get_user(signature: str) -> CreateUserData:
    return await get_user(signature)

@ovs.get("/users")
async def ovs_api_get_users() -> List[CreateUserData]:
    return await get_users()

@ovs.delete("/user")
async def ovs_api_delete_user(signature: str) -> None:
    return await delete_user(signature)

### Polls

@ovs.post("/poll")
async def ovs_api_create_poll(data: CreatePollData)
    return await create_poll(data)

@ovs.get("/poll")
async def ovs_api_get_poll(poll_id: str):
    return await get_poll(poll_id)

@ovs.get("/polls")
async def ovs_api_get_polls():
    return await get_polls()

# Needs signture of person who created poll
@ovs.delete("/poll")
async def ovs_api_delete_poll(signature: str) -> None:
    return await delete_poll()

### Approvals

@ovs.post("/approval")
async def ovs_api_create_approval(data: CreateVoteApprovalData):
    return await create_approval(data)

@ovs.post("/approval")
async def ovs_api_check_approval(poll_id: str) -> CreateVoteApprovalData:
    row = await db.fetchone("SELECT * FROM ovs.Approvals WHERE poll_id = ?", (poll_id,))
    return CreateVoteApprovalData(**row) if row else None


### Votes


async def create_vote(data: CreateVoteData, inkey: Optional[str] = "") -> CreateVoteData:
    checkApprovals = await check_approval(data.poll_id)
    if len(checkApprovals) < 3:
        return False
    voteCheck = await check_vote(data.user_id)
    if voteCheck:
        return False
    voteCheck_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.VoteCheck (
            id,
            poll_id, 
            user_id
        )
        VALUES (?, ?, ?)
        """,
        (voteCheck_id, data.poll_id, data.user_id),
    )
    await db.execute(
        """
        INSERT INTO ovs.Vote (
            id,
            poll_id,
            vote_opt
        )
        VALUES (?, ?, ?)
        """,
        (data.signature, data.poll_id, data.vote_opt),
    )
    return await get_vote(data.signature)


async def get_vote(vote_id: str) -> CreateVoteData:
    row = await db.fetchone("SELECT * FROM ovs.VoteCheck WHERE id = ?", (vote_id,))
    return CreateVoteData(**row) if row else None

async def check_vote(user_id: str) -> CreateVoteData:
    row = await db.fetchone("SELECT * FROM ovs.VoteCheck WHERE user_id = ?", (user_id,))
    return CreateVoteData(**row) if row else None


if __name__ == "__main__":
    uvicorn.run(ovs, host="0.0.0.0", port=8000)
