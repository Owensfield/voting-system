from models import CreateUserData, CreatePollData, CreateVoteData, CreateVoteApprovalData
from typing import Optional, Dict
from typing import List, Optional, Union
import shortuuid
from db import Database
from http import HTTPStatus
from fastapi import HTTPException
db = Database("ovs")
### Users


async def create_user(
    data: CreateUserData
) -> CreateUserData:
    user = await get_user_by_email(data.email)
    if user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User {data.email}, already exists",
            )
    user_id = shortuuid.uuid()
    await db.execute(
        """
        INSERT INTO Users (
            id,
            email,
            passhash,
            roll
        )
        VALUES (?, ?, ?, ?)
        """,
        (user_id, data.email, data.passhash, data.roll,),
    )
    return await get_user(user_id)

async def get_user(passhash: str) -> CreateUserData:
    row = await db.fetchone("SELECT * FROM Users WHERE passhash = ?", (passhash,))
    return CreateUserData(**row) if row else None

async def get_user_by_email(email: str) -> CreateUserData:
    row = await db.fetchone("SELECT * FROM Users WHERE email = ?", (email,))
    return CreateUserData(**row) if row else None

async def get_users() -> List[CreateUserData]:
    rows = await db.fetchall("SELECT * FROM Users")
    return [CreateUserData(**row) for row in rows]

async def delete_user(passhash: str) -> None:
    user = await get_user(passhash)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User doesnt exist",
            )
    await db.execute("DELETE FROM Users WHERE passhash = ?", (passhash,))


### Polls


async def create_poll(data: CreatePollData, inkey: Optional[str] = "") -> CreatePollData:
    poll_id = shortuuid.uuid()
    await db.execute(
        """
        INSERT INTO Polls (
            id,
            signature,
            title,
            opt1 , 
            opt2, 
            opt3, 
            opt4, 
            opt5, 
            active,
            closing_date,
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            poll_id,
            data.signature,
            data.title,
            data.opt1,
            data.opt2,
            data.opt3,
            data.opt4,
            data.opt5,
            data.active,
            data.closing_date,
        ),
    )
    return await get_poll(poll_id)

async def get_poll(poll_id: str) -> CreatePollData:
    row = await db.fetchone("SELECT * FROM Polls WHERE id = ?", (poll_id,))
    return CreatePollData(**row) if row else None

async def get_polls(poll: str) -> List[CreatePollData]:
    rows = await db.fetchall("SELECT * FROM Polls", (poll,))
    return [CreatePollData(**row) for row in rows]

# Needs signture of person who created poll
async def delete_poll(signature: str) -> None:
    await db.execute("DELETE FROM Polls WHERE signature = ?", (signature,))


### Approvals


async def create_approval(data: CreateVoteApprovalData) -> CreateVoteApprovalData:
    poll = await check_approval(data.poll_id)
    if poll.user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User has already approved",
            )

    approval_id = shortuuid.uuid()
    await db.execute(
        """
        INSERT INTO Approvals (
            id,
            poll_id,
            user_id,
        )
        VALUES (?, ?, ?)
        """,
        (
            approval_id,
            data.poll_id,
            data.user_id,
        ),
    )
    return await get_poll(poll_id)
    
async def check_approval(poll_id: str) -> CreateVoteApprovalData:
    row = await db.fetchone("SELECT * FROM Approvals WHERE poll_id = ?", (poll_id,))
    return CreateVoteApprovalData(**row) if row else None


### Votes


async def create_vote(data: CreateVoteData, inkey: Optional[str] = "") -> CreateVoteData:
    checkApprovals = await check_approval(data.poll_id)
    if len(checkApprovals) < 3:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Poll needs {3 - len(checkApprovals)} more approvals",
            )
    voteCheck = await check_vote(data.user_id)
    if voteCheck:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User has already voted",
            )
    voteCheck_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO VoteCheck (
            id,
            poll_id, 
            user_id
        )
        VALUES (?, ?, ?)
        """,
        (voteCheck_id, data.poll_id, data.user_id,),
    )
    await db.execute(
        """
        INSERT INTO Vote (
            id,
            poll_id,
            vote_opt
        )
        VALUES (?, ?, ?)
        """,
        (data.signature, data.poll_id, data.vote_opt,),
    )
    return await get_vote(data.signature)


async def get_vote(vote_id: str) -> CreateVoteData:
    row = await db.fetchone("SELECT * FROM VoteCheck WHERE id = ?", (vote_id,))
    return CreateVoteData(**row) if row else None

async def get_vote_poll(poll_id: str) -> CreateVoteData:
    row = await db.fetchone("SELECT * FROM VoteCheck WHERE poll_id = ?", (poll_id,))
    return CreateVoteData(**row) if row else None

async def check_vote(user_id: str) -> CreateVoteData:
    row = await db.fetchone("SELECT * FROM VoteCheck WHERE user_id = ?", (user_id,))
    return CreateVoteData(**row) if row else None