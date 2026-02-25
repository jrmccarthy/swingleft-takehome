import ipdb
import pytest
from pytest_sqlalchemy import connection
from engine import get_row, get_rows
from datetime import date
from models import VoterRegDeadline

def test_session(dbsession):
    assert dbsession

def test_get_row(engine):
    # Get back a row and all the data matches our expectations from the fixture
    row = get_row(engine, state="Illinois")
    assert(row)
    assert(row.state) == "Illinois"
    assert(row.deadline_in_person) == date.fromisoformat("2026-10-01")
    assert(row.deadline_by_mail) == date.fromisoformat("2026-10-01")
    assert(row.deadline_online) == date.fromisoformat("2026-10-01")
    assert(row.election_day_registration) == "In-person on Election Day"
    assert(row.online_registration_link) == "https://illiois.test.com"
    assert(row.description) == "Some other details about this state"

def test_get_row_none(engine):
    # Filter for a nonexistent state and expect an empty response but no exception
    row = get_row(engine, state="foo")
    assert row == None

def test_get_rows(engine):
    # Get back all the rows and make sure they are all returned
    rows = get_rows(engine)
    assert len(rows) == 5

def test_get_rows_filter_state(engine):
    # Filter on equality for the state field
    filter_by = "state"
    filter_op = "eq"
    filter_value = "Illinois"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 1
    assert rows[0].state == "Illinois"

def test_get_rows_filter_date(engine):
    # Filter on equality for a Date type field
    filter_by = "deadline_in_person"
    filter_op = "eq"
    filter_value = "2026-10-01"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 1
    assert rows[0].state == "Illinois"

def test_get_rows_filter_online_reg_link(engine):
    # Filter on equality for a String field that isn't a PK
    filter_by = "election_day_registration"
    filter_op = "eq"
    filter_value = "In-person on Election Day"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 3
    assert rows[0].state == "Illinois"
    assert rows[1].state == "New York"
    assert rows[2].state == "Washington"

def test_get_rows_filter_date_lt(engine):
    # Test the < operator for dates
    filter_by = "deadline_in_person"
    filter_op = "lt"
    filter_value = "2026-10-02"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 1
    assert rows[0].state == "Illinois"

def test_get_rows_filter_date_lte(engine):
    # Test the <= operator for dates
    filter_by = "deadline_by_mail"
    filter_op = "lte"
    filter_value = "2026-10-02"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 2
    assert rows[0].state == "Illinois"
    assert rows[1].state == "New York"

def test_get_rows_filter_date_gt(engine):
    # Test the > operator for dates
    filter_by = "deadline_online"
    filter_op = "gt"
    filter_value = "2026-10-03"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 2
    assert rows[0].state == "Indiana"
    assert rows[1].state == "Washington"

def test_get_rows_filter_date_gte(engine):
    # Test the >= operator for dates
    filter_by = "deadline_online"
    filter_op = "gte"
    filter_value = "2026-10-03"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 3
    assert rows[0].state == "Indiana"
    assert rows[1].state == "New York"
    assert rows[2].state == "Washington"

def test_get_rows_filter_date_ne(engine):
    # Test the != operator for dates
    filter_by = "deadline_by_mail"
    filter_op = "ne"
    filter_value = "2026-10-01"
    rows = get_rows(engine, filter_by=filter_by, filter_op=filter_op, filter_value=filter_value)
    assert len(rows) == 2
    assert rows[0].state == "Indiana"
    assert rows[1].state == "Washington"

def test_get_rows_order_by_state(engine):
    # Ensure we can sort by state
    order_by = VoterRegDeadline.state
    rows = get_rows(engine, order_by=order_by)
    assert len(rows) == 5
    assert rows[0].state == "Alabama"
    assert rows[1].state == "Illinois"
    assert rows[2].state == "Indiana"
    assert rows[3].state == "New York"
    assert rows[4].state == "Washington"

def test_get_rows_order_by_state_desc(engine):
    # Ensure we can sort by state, descending
    order_by = VoterRegDeadline.state
    rows = get_rows(engine, order_by=order_by, sort_order="desc")
    assert len(rows) == 5
    assert rows[0].state == "Washington"
    assert rows[1].state == "New York"
    assert rows[2].state == "Indiana"
    assert rows[3].state == "Illinois"
    assert rows[4].state == "Alabama"

def test_get_rows_order_by_date(engine):
    # Ensure we can order by a date field, and NULL are returned at the end
    order_by = VoterRegDeadline.deadline_in_person
    rows = get_rows(engine, order_by=order_by)
    assert len(rows) == 5
    assert rows[0].state == "Illinois"
    assert rows[1].state == "New York"
    assert rows[2].state == "Washington"
    assert rows[3].state == "Indiana"
    assert rows[4].state == "Alabama"

def test_get_rows_order_by_date_desc(engine):
    # Ensure we can order by a date field descending, and NULL are returned at the start
    order_by = VoterRegDeadline.deadline_in_person
    rows = get_rows(engine, order_by=order_by, sort_order="desc")
    assert len(rows) == 5
    assert rows[0].state == "Alabama"
    assert rows[1].state == "Indiana"
    assert rows[2].state == "Washington"
    assert rows[3].state == "New York"
    assert rows[4].state == "Illinois"

def test_get_rows_order_by_date_default_is_asc(engine):
    # Ensure the default sort is ascending
    order_by = VoterRegDeadline.deadline_in_person
    rows = get_rows(engine, order_by=order_by, sort_order="asc")
    unsorted_rows = get_rows(engine, order_by=order_by)
    for (row, unsorted_row) in zip(rows, unsorted_rows):
        assert row.state == unsorted_row.state
