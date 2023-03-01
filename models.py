import enum

from sqlalchemy import Integer, Float, ForeignKey, Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import datetime

db = declarative_base()

class StatusEnum(enum.Enum):
    accepted = "accepted"
    declined = "declined"
    not_processed = "not_processed"

class UserModel(db):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, unique=True)
    amount = Column(Float)
    transactions = relationship('TransactionModel', backref='usermodel', cascade='all,delete-orphan')

    def __repr__(self):
        line = ""
        for tr in self.transactions:
            line += f"{tr}\n"
        # return f"User: {self.id}\nAmount: {self.amount}\n{line}"
        return f"User: {self.id}\nAmount: {self.amount}\n"


class TransactionModel(db):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    user_id = Column(UUID, ForeignKey(UserModel.id))
    time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(StatusEnum))

    def __str__(self):
        return f"Transaction: {self.id}\n amount: {self.amount}\n user_id: {self.user_id}\n{'*' * 10}\ntime: {self.time}"

    def __repr__(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'user_id': self.user_id,
            'time': self.time
        }

