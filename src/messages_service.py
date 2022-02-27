from fastapi import FastAPI


messages_service = FastAPI()


@messages_service.get("/")
def get_messages():
    return "message-service is not implemented yet"