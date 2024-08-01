from typing import List
from pydantic import BaseModel


class RpcParam(BaseModel):
    rpc_id: str
    user_id: str
    param: List[object]
    is_one: int
