from email import header
from fastapi import FastAPI, Request, Response, status

import uuid
import requests
import yaml
import json
import os

from constants import LOGGING, MESSAGES

facade_service = FastAPI()

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "services_config.yml")
config = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.FullLoader)
LOGGING_URI = f"http://{config[LOGGING]['host']}:{config[LOGGING]['port']}"
MESSAGES_URI = f"http://{config[MESSAGES]['host']}:{config[MESSAGES]['port']}"


@facade_service.post("/")
async def post_message(message: Request):
    body = await message.body()
    
    logging_data = {
        "uuid": str(uuid.uuid1()),
        "message": body.decode()
    }
    logging_data = json.dumps(logging_data)
    requests.post(LOGGING_URI, data=logging_data)


@facade_service.get("/")
async def get_message(response: Response):
    try:
        logging_response = requests.get(LOGGING_URI)
        messages_response = requests.get(MESSAGES_URI)
    except Exception as exc:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return f"Error happened in internal communication between services: {exc}"
    
    if logging_response.status_code != 200:
        response.status_code = logging_response.status_code
        return f"logging service failed with code: {logging_response.status_code}; error: {logging_response.text}"
    elif messages_response.status_code != 200:
        response.status_code = messages_response.status_code
        return f"messages service failed with code: {messages_response.status_code}; error: {logging_response.text}"
    
    return f"{logging_response.text}: {messages_response.text}"
