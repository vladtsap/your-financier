from dataclasses import replace
from datetime import datetime

from flask import Flask, request, Response
from flask.json import JSONEncoder
from pytz import timezone
from werkzeug.exceptions import BadRequest, HTTPException, ServiceUnavailable, NotFound

from models.core import Transaction, Categories
from utils.mongo import MongoTransaction


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


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


@app.route('/webhook/<budget_id>/<member_id>', methods=['GET', 'POST'])
def webhook(budget_id, member_id):
    if request.method == 'GET':
        return Response()

    elif request.method == 'POST':
        if not (content := request.json):
            raise BadRequest('not JSON format')

        transaction = process_transaction(
            budget_id=budget_id,
            member_id=int(member_id),
            data=content['data']['statementItem'],
        )

        MongoTransaction().add(transaction)

        # TODO: send notification to group
    return Response()

#
#
# @app.errorhandler(HTTPException)
# def _(e: HTTPException):
#     return {'message': e.description}, e.code
#
#
# @app.errorhandler(CloudResourceNotReadyException)
# def _(_):
#     return {'message': 'resource is not ready yet'}, 202
