from dataclasses import replace
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel
from pytz import timezone

from config import bot
from models.core import Transaction, Categories
from utils.mongo import MongoTransaction

app = FastAPI()


class Item(BaseModel):
    time: int
    mcc: int
    amount: int


class Data(BaseModel):
    account: str
    statementItem: Item


class Object(BaseModel):
    type: str
    data: Data


@app.get('/webhook/{budget_id}/{member_id}')
def test_webhook():
    return Response()


@app.post('/webhook/{budget_id}/{member_id}')
async def process_transaction(budget_id: str, member_id: int, obj: Object):
    item = obj.data.statementItem

    transaction = Transaction(
        budget_id=budget_id,
        member_id=member_id,
        date=timezone('UTC').localize(
            datetime.utcfromtimestamp(item.time)
        ).astimezone(timezone('Europe/Kiev')),
        category=Categories.match(item.mcc),
    )

    if (amount := item.amount) > 0:
        transaction = replace(transaction, income=amount / 100)
    else:
        transaction = replace(transaction, outcome=abs(amount) / 100)

    MongoTransaction().add(transaction)

    await bot.send_message(
        chat_id=member_id,
        text=transaction.message_view,
    )

    return Response()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
