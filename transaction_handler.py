import time

from config import postgres_settings
from db_utils import get_engine_from_settings, get_session
from models import UserModel, TransactionModel, StatusEnum

engine = get_engine_from_settings(postgres_settings)


def handler():
    while True:
        try:

            session = get_session(engine)
            tr = session.query(TransactionModel).filter(TransactionModel.status == StatusEnum.not_processed).order_by(TransactionModel.time).first()
            # print(tr)
            if tr is None:
                continue
            user = session.query(UserModel).filter(UserModel.id == tr.user_id).first()
            # print(user.amount)
            if tr.amount < 0:
                if user.amount > -tr.amount:
                    user.amount += tr.amount
                    tr.status = StatusEnum.accepted
                    session.add_all([user, tr])
                else:
                    tr.status = StatusEnum.declined
            else:
                user.amount += tr.amount
                tr.status = StatusEnum.accepted
                session.add_all([user, tr])
            # print(user.amount)
            session.commit()
            session.close()

        except Exception as e:
            print(e)
        finally:
            continue


if __name__ == '__main__':
    handler()