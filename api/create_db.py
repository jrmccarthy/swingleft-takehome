import csv

from models import VoterRegDeadline
from engine import initialize_engine, initialize_tables, add_row, create_db

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
    print("Creating tables and inserting data")
    engine = initialize_engine()
    create_db(engine)
    initialize_tables(engine)
    rows = read_csv()
    for row in rows:
        add_row(engine, row)

