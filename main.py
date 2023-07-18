from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import pickle
import base64
import requests
import json

INFERENCE_API = "http://localhost:8000"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": f"Hello from team Invictus!"}


def tensor_to_base64(arr):
    bt = str(arr.tolist()).encode("utf-8")
    encoded_bytes = base64.b64encode(bt)
    encoded_string = encoded_bytes.decode('utf-8')

    return encoded_string


class PromptModel(BaseModel):
    prompt: str


@app.post("/prove")
async def prove(prompt: PromptModel):
    inference_api_endpoint = f"{INFERENCE_API}/inference"

    headers = {'Content-Type': 'application/json'}

    resp = requests.post(
        inference_api_endpoint,
        headers=headers,
        data=json.dumps({"prompt": prompt.prompt})
    )

    op = resp.json()

