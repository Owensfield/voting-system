from models import CreateUserData, CreatePollData, CreateVoteData, CreateVoteApprovalData, GetPollData
from typing import Optional, Dict
from typing import List, Optional, Union
import shortuuid
import time
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
    passhash = await get_user_by_passhash(data.passhash)
    if passhash:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Passhash already exists",
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

async def get_user(user_id: str) -> CreateUserData:
    row = await db.fetchone("SELECT * FROM Users WHERE id = ?", (user_id,))
    return CreateUserData(**row) if row else None

async def get_user_by_passhash(passhash: str) -> CreateUserData:
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
    poll_id = shortuuid.uuid(data.title)
    pollCheck = await get_poll(poll_id)
    if pollCheck:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Poll with title {data.title} already exists",
            )
    polls = await get_polls_by_signature(data.signature)
    monthCount = 0
    for poll in polls:
        if (int(time.time()) - poll.timestamp) < 2629743:
            monthCount = monthCount + 1
    if monthCount > 2:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Users are only allowed to suggest 3 polls per month",
            )
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
            closing_date
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
            0,
            data.closing_date,
        ),
    )
    return await get_poll(poll_id)

async def get_poll(poll_id: str) -> GetPollData:
    row = await db.fetchone("SELECT * FROM Polls WHERE id = ?", (poll_id,))
    return GetPollData(**row) if row else None

async def get_polls_by_signature(signature: str) -> CreatePollData:
    rows = await db.fetchall("SELECT * FROM Polls WHERE signature = ?", (signature,))
    return [CreatePollData(**row) for row in rows]

async def get_polls() -> List[GetPollData]:
    rows = await db.fetchall("SELECT * FROM Polls")
    return [GetPollData(**row) for row in rows]

# Needs signture of person who created poll
async def delete_poll(signature: str, poll_id: str) -> None:
    polls = await get_polls_by_signature(signature)
    for poll in polls:
        if poll.id == poll_id:
            return await db.execute("DELETE FROM Polls WHERE id = ?", (poll_id,))
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User doesny have permission to delete this poll",
            )
    


### Approvals


async def create_approval(data: CreateVoteApprovalData) -> CreateVoteApprovalData:
    user = await get_user_by_passhash(data.passhash)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User doesnt exist",
            )
    
    poll = await get_poll(data.poll_id)
    if not poll:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Poll does not exist",
            )
    approvals = await check_approvals(data.poll_id)
    if approvals:
        for approval in approvals:
            if approval.user_id == data.user_id:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail=f"User has already approved",
                    )
    if user.roll != 2:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"User must be on the steering group to approve",
            )
    
    approval_id = shortuuid.uuid()
    await db.execute(
        """
        INSERT INTO Approvals (
            id,
            poll_id,
            passhash
        )
        VALUES (?, ?, ?)
        """,
        (
            approval_id,
            data.poll_id,
            data.passhash,
        ),
    )

    return await get_poll(poll_id)
    
async def check_approvals(poll_id: str) -> CreateVoteApprovalData:
    rows = await db.fetchall("SELECT * FROM Approvals WHERE poll_id = ?", (poll_id,))
    if not rows:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Poll has no approvals",
        )
    [CreateVoteApprovalData(**row) for row in rows]


### Votes


async def create_vote(data: CreateVoteData, inkey: Optional[str] = "") -> CreateVoteData:
    checkApprovals = await check_approval(data.poll_id)
    if len(checkApprovals) < 3:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"Poll needs {3 - len(checkApprovals)} more approvals",
            )
    voteCheck = await check_votes(data.user_id)
    for vote in voteCheck:
        if vote:
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
    row = await db.fetchone("SELECT * FROM Vote WHERE id = ?", (vote_id,))
    return CreateVoteData(**row) if row else None

async def get_votes_poll(poll_id: str) -> CreateVoteData:
    rows = await db.fetchall("SELECT * FROM Vote WHERE poll_id = ?", (poll_id,))
    return [CreateVoteData(**row) for row in rows]

async def check_votes(user_id: str) -> CreateVoteData:
    row = await db.fetchall("SELECT * FROM VoteCheck WHERE user_id = ?", (user_id,))
    return [CreateVoteData(**row) for row in rows]