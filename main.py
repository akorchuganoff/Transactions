from uuid import uuid4

from fastapi import FastAPI, Query, HTTPException, Response

from config import postgres_settings
from db_utils import get_engine_from_settings, get_session
from models import UserModel, TransactionModel, StatusEnum
from schemas import Transaction, User

app = FastAPI()
engine = get_engine_from_settings(postgres_settings)


@app.get("/")
def read_root():
    return "Выполнил Александр Корчуганов"


@app.post("/user")
def create_user(item: User):
    session = get_session(engine)
    try:
        user = UserModel(id=uuid4(), amount=item.amount)
        session.add(user)
        session.commit()
        return {'id': user.id, 'amount': user.amount}
    except Exception as ex:
        raise HTTPException(500, detail=str(ex))
    finally:
        session.close()


@app.post("/transaction")
def make_transaction(item: Transaction):
    session = get_session(engine)
    try:
        user_id = item.user_id
        amount = item.amount

        transaction = TransactionModel(
            amount=amount,
            user_id=user_id,
            status=StatusEnum.not_processed
        )

        session.add(transaction)
        session.commit()
        return Response(status_code=201)

    except Exception as ex:
        raise HTTPException(500, detail=str(ex))
    finally:
        session.close()


@app.get("/all")
def get_all_transactions_by_id(q: str = Query(...)):
    session = get_session(engine)
    try:
        user = session.query(UserModel).filter(UserModel.id == q).first()
        result = {
            'transactions': []
        }

        for tr in user.transactions:
            result['transactions'].append(tr)
        return result
    except Exception as ex:
        raise HTTPException(500, detail=str(ex))
    finally:
        session.close()
