from engine import CONNECTION_URL, add_row, create_db, drop_db, initialize_tables
from models import VoterRegDeadline
import pytest
from sqlalchemy import create_engine

TEST_DB = "testdb"
TEST_ROWS = [
    ["Illinois", "2026-10-01", "2026-10-01", "2026-10-01", "In-person on Election Day", "https://illiois.test.com", "Some other details about this state"],
    ["Alabama", None, None, None, "", "", "Some other details about this state"],
    ["Washington", "2026-11-03", "2026-11-04", "2026-11-05", "In-person on Election Day", "https://washington.test.com", ""],
    ["Indiana", "2026-11-06", "2026-11-05", "2026-10-04", "In-person during early voting", "https://indiana.test.com", "Some other details about this state"],
    ["New York", "2026-11-01", "2026-10-01", "2026-10-03", "In-person on Election Day", "https://newyork.test.com", "More stuff"],
]


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    engine = create_engine(f"{CONNECTION_URL}/{TEST_DB}")
    test_db_setup(engine)
    initialize_tables(engine)
    for row in TEST_ROWS:
        add_row(engine, VoterRegDeadline(
            state=row[0],
            deadline_in_person=row[1] or None,
            deadline_by_mail=row[2] or None,
            deadline_online=row[3] or None,
            election_day_registration=row[4],
            online_registration_link=row[5],
            description=row[6],
        ))


def test_db_setup(engine):
    drop_db(engine)
    create_db(engine)


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return f"{CONNECTION_URL}/{TEST_DB}"
