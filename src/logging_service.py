from fastapi import FastAPI
from pydantic import BaseModel
from multiprocessing import Manager


logging_service = FastAPI()


class Message(BaseModel):
    uuid: str
    message: str

manager = Manager()
storage = manager.dict()

@logging_service.post("/")
def post_log(msg: Message):
    print(f"Add {msg.uuid}  ->  {msg.message}")
    storage[msg.uuid] = msg.message


@logging_service.get("/")
def get_log():
    return str(list(storage.values()))
