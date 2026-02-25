import csv

from engine import add_row, create_db, initialize_engine, initialize_tables
from models import VoterRegDeadline


def read_csv(filename="voter_registration_deadlines_2026.csv"):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        rows = []
        for row in reader:
            rows.append(VoterRegDeadline(
                state=row[0],
                deadline_in_person=row[1] or None,
                deadline_by_mail=row[2] or None,
                deadline_online=row[3] or None,
                election_day_registration=row[4],
                online_registration_link=row[5],
                description=row[6],
            ))
    return rows


if __name__ == "__main__":
    print("Attempting to create tables and insert data")
    engine = initialize_engine()
    if create_db(engine):
        print("Database created, inserting data now")
        initialize_tables(engine)
        rows = read_csv()
        for row in rows:
            add_row(engine, row)
    else:
        print("Database already exists, run drop_db first if you want to recreate")
