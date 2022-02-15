from models import CreateUserData, CreatePollData, CreateVoteData, CreateVoteApprovalData
from typing import Optional, Dict
from typing import List, Optional, Union

### Users


async def create_user(
    data: CreateUserData, inkey: Optional[str] = ""
) -> CreateUserData:
    user_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Users (
            id,
            email, 
            roll
        )
        VALUES (?, ?, ?)
        """,
        (user_id, data.email, data.roll),
    )
    return await get_user(user_id)

async def get_user(userhash: str) -> CreateUserData:
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (userhash,))
    return CreateUserData(**row) if row else None

async def get_users() -> List[CreateUserData]:
    rows = await db.fetchall("SELECT * FROM ovs.Users")
    return [CreateUserData(**row) for row in rows]

async def delete_user(user_id: str) -> None:
    await db.execute("DELETE FROM ovs.Users WHERE id = ?", (user_id,))


### Polls


async def create_poll(data: CreatePollData, inkey: Optional[str] = "") -> CreatePollData:
    poll_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Polls (
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
    row = await db.fetchone("SELECT * FROM ovs.Polls WHERE id = ?", (poll_id,))
    return CreatePollData(**row) if row else None

async def get_polls(poll: str) -> List[CreatePollData]:
    rows = await db.fetchall("SELECT * FROM ovs.Polls", (poll,))
    return [CreatePollData(**row) for row in rows]

# Needs signture of person who created poll
async def delete_poll(signature: str) -> None:
    await db.execute("DELETE FROM ovs.Polls WHERE signature = ?", (signature,))


### Approvals


async def create_approval(data: CreateVoteApprovalData) -> CreateVoteApprovalData:
    approval_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Approvals (
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