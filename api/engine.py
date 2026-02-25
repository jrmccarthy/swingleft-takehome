import os
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy_utils import database_exists, create_database, drop_database
from enum import StrEnum
from typing import Tuple

import models
import ipdb

DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Password1!")
DB_HOST = os.getenv("DB_HOST", "localhost:5432")

CONNECTION_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
CONNECTION_DB = "state_registration_deadlines"
CONNECTION_STRING = f"{CONNECTION_URL}/{CONNECTION_DB}"

class FilterOpsEnum(StrEnum):
    eq = "eq"
    lt = "lt"
    lte = "lte"
    gt = "gt"
    gte = "gte"

type filter_ops = FilterOpsEnum
type filter_arg = Tuple[InstrumentedAttribute, filter_ops, str]

def initialize_engine():
    return create_engine(CONNECTION_STRING, echo=True)

def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)

def drop_db(engine):
    if database_exists(engine.url):
        drop_database(engine.url)

def initialize_tables(engine):
    models.Base.metadata.create_all(engine)

def add_row(engine, row):
    with Session(engine) as session:
        session.add(row)
        session.commit()

def get_row(engine, state):
    with Session(engine) as session:
        q = select(models.VoterRegDeadline).where(models.VoterRegDeadline.state == state)
        try:
            return session.scalars(q).one()
        except NoResultFound:
            return None

def get_rows(engine, filter_by: InstrumentedAttribute=None, filter_op: filter_ops=None, filter_value: str=None, order_by: InstrumentedAttribute=None, sort_order=None):
    with Session(engine) as session:
        q = select(models.VoterRegDeadline)
        if filter_by and filter_op and filter_value:
            try:
                if filter_by in ["deadline_by_mail", "deadline_in_person", "deadline_online"]:
                    assert date.fromisoformat(filter_value)
                match filter_op:
                    case FilterOpsEnum.eq:
                        q = q.where(getattr(models.VoterRegDeadline, filter_by) == filter_value)
                    case FilterOpsEnum.lt:
                        q = q.where(getattr(models.VoterRegDeadline, filter_by) < filter_value)
                    case FilterOpsEnum.lte:
                        q = q.where(getattr(models.VoterRegDeadline, filter_by) <= filter_value)
                    case FilterOpsEnum.gt:
                        q = q.where(getattr(models.VoterRegDeadline, filter_by) > filter_value)
                    case FilterOpsEnum.gte:
                        q = q.where(getattr(models.VoterRegDeadline, filter_by) >= filter_value)
                    case _:
                        raise Exception(f"Operator not allowed: provided {filter[1]}")
            except ValueError:
                # Invalid date, we're pretty permissive so just don't filter in this case
                pass
        if order_by:
            if sort_order == "desc":
                q = q.order_by(order_by.desc())
            else:
                q = q.order_by(order_by.asc())
        else:
            q = q.order_by(models.VoterRegDeadline.state.asc())
        
        return session.scalars(q).all()