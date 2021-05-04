from dataclasses import replace
from datetime import datetime
from json import JSONDecodeError

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from pytz import timezone

from config import bot
from models.core import Transaction, Categories
from utils.mongo import MongoTransaction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def process_transaction(budget_id: str, member_id: int, data: dict) -> Transaction:
    transaction = Transaction(
        budget_id=budget_id,
        member_id=member_id,
        date=timezone('UTC').localize(
            datetime.utcfromtimestamp(data['time'])
        ).astimezone(timezone('Europe/Kiev')),
        category=Categories.match(data['mcc']),
    )

    if (amount := data['amount']) > 0:
        transaction = replace(transaction, income=amount / 100)
    else:
        transaction = replace(transaction, outcome=abs(amount) / 100)

    return transaction


@app.get('/webhook/{budget_id}/{member_id}')
def ping(budget_id: str, member_id: int):
    return {'status': 'ok'}


@app.post('/webhook/{budget_id}/{member_id}')
async def webhook(budget_id: str, member_id: int, request: Request):
    content = await request.json()

    transaction = process_transaction(
        budget_id=budget_id,
        member_id=member_id,
        data=content['data']['statementItem'],
    )

    MongoTransaction().add(transaction)
    await bot.send_message(
        chat_id=member_id,
        text=transaction.message_view,
    )

    # TODO: send notification to group
    return Response()


@app.exception_handler(JSONDecodeError)
async def handle_not_json_error(request: Request, exc: JSONDecodeError):
    return PlainTextResponse('not JSON format', status_code=400)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
