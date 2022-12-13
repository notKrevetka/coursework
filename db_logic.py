from sqlalchemy import create_engine, inspect, select
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Numeric, Boolean, Time

DBFILEPATH = 'sqlite:///db.db'

engine = create_engine(DBFILEPATH, echo=True)
meta = MetaData()

tests_results = Table(
    'tests_results', meta,
    Column('counter', Integer, primary_key=True),
    Column('user', String),
    Column('time_current', Integer),
    Column('type_action', String),
    Column('source_index', Integer),
    Column('destination_index', Integer),
    sqlite_autoincrement=True
)


user_levels = Table(
    'user_levels', meta,
    Column('user', String, primary_key=True),
    Column('level', Integer),
)
meta.create_all(engine)

def record_users_action(user,time_current, type_action, source_index, destination_index):
    with engine.connect() as conn:
        stmt1 = tests_results.insert().values(user=user, time_current=time_current, type_action=type_action, source_index=source_index, destination_index=destination_index)
        conn.execute(stmt1)

def set_user_level(user, level):
    with engine.connect() as conn:
        stmt = user_levels.insert().values(user=user, level=level)
        conn.execute(stmt)