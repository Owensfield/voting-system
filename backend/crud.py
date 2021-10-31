### Users


async def create_user(data: CreateUserData, inkey: Optional[str] = "") -> User:
    user_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Users (
            id,
            username, 
            hash,
            roll,
        )
        VALUES (?, ?, ?, ?)
        """,
        (user_id, data.username, data.hash, data.roll),
    )
    return await get_user(user_id)


async def update_user(
    data: CreateUserData, user_id: Optional[str] = ""
) -> Optional[Users]:
    q = ", ".join([f"{field[0]} = ?" for field in data])
    items = [f"{field[1]}" for field in data]
    items.append(user_id)
    await db.execute(f"UPDATE ovs.Users SET {q} WHERE id = ?", (items))
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (user_id,))
    return Users(**row) if row else None


async def get_user(user_id: str) -> Users:
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (user_id,))
    return Users(**row) if row else None


async def get_users(user: str) -> List[Users]:
    rows = await db.fetchall("SELECT * FROM ovs.Users WHERE user = ?", (user,))
    return [Users(**row) for row in rows]


async def delete_user(user_id: str) -> None:
    await db.execute("DELETE FROM ovs.Users WHERE id = ?", (user_id,))


### Polls


async def create_poll(data: CreatePollData, inkey: Optional[str] = "") -> User:
    poll_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Users (
            id,
            title, 
            opt1 , 
            opt2, 
            opt3, 
            opt4, 
            opt5, 
            approvals_csv,
            active,
            closing_date,
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            poll_id,
            data.title,
            data.opt1,
            data.opt2,
            data.opt3,
            data.opt4,
            data.opt5,
            data.approvals_csv,
            data.active,
            data.closing_date,
        ),
    )
    return await get_poll(poll_id)


async def update_poll(
    data: CreatePollData, poll_id: Optional[str] = ""
) -> Optional[Polls]:
    q = ", ".join([f"{field[0]} = ?" for field in data])
    items = [f"{field[1]}" for field in data]
    items.append(poll_id)
    await db.execute(f"UPDATE ovs.Users SET {q} WHERE id = ?", (items))
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (poll_id,))
    return Polls(**row) if row else None


async def get_poll(poll_id: str) -> Polls:
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (poll_id,))
    return Polls(**row) if row else None


async def get_polls(poll: str) -> List[Polls]:
    rows = await db.fetchall("SELECT * FROM ovs.Users WHERE poll = ?", (poll,))
    return [Polls(**row) for row in rows]


async def delete_poll(poll_id: str) -> None:
    await db.execute("DELETE FROM ovs.Users WHERE id = ?", (poll_id,))


### Votes


async def create_vote(data: CreateUserData, inkey: Optional[str] = "") -> User:
    vote_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO ovs.Users (
            id,
            vote_id, 
            user_id, 
            vote_opt,
        )
        VALUES (?, ?, ?, ?)
        """,
        (user_id, data.vote_id, data.user_id, data.vote_opt),
    )
    return await get_vote(vote_id)


async def update_vote(
    data: CreateUserData, vote_id: Optional[str] = ""
) -> Optional[Users]:
    q = ", ".join([f"{field[0]} = ?" for field in data])
    items = [f"{field[1]}" for field in data]
    items.append(vote_id)
    await db.execute(f"UPDATE ovs.Users SET {q} WHERE id = ?", (items))
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (vote_id,))
    return Users(**row) if row else None


async def get_vote(vote_id: str) -> Users:
    row = await db.fetchone("SELECT * FROM ovs.Users WHERE id = ?", (vote_id,))
    return Users(**row) if row else None


async def get_votes_poll(poll_id: str) -> List[Users]:
    rows = await db.fetchall("SELECT * FROM ovs.Users WHERE poll_id = ?", (poll_id,))
    return [Users(**row) for row in rows]


async def delete_vote(vote_id: str) -> None:
    await db.execute("DELETE FROM ovs.Users WHERE id = ?", (vote_id,))
