from starlette.requests import Request
from fastapi.param_functions import Query
from typing import Optional, Dict
from pydantic import BaseModel
import json
from sqlite3 import Row


class CreateUserData(BaseModel):
    username: str = Query(None)
    user_hash: str = Query(None)
    roll: int = Query(0)


class CreatePollData(BaseModel):
    title: str = Query(None)
    opt1: str = Query(None)
    opt2: str = Query(None)
    opt3: str = Query(None)
    opt4: str = Query(None)
    opt5: str = Query(None)
    approvals_csv: str = Query(None)
    active: int = Query(0)
    closing_date: int = Query(0)


class CreateVoteData(BaseModel):
    vote_id: str = Query(None)
    user_id: str = Query(None)
    vote_opt: str = Query(None)

