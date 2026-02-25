import csv

from models import VoterRegDeadline
from engine import initialize_engine, drop_db

if __name__ == "__main__":
    print("Dropping database")
    engine = initialize_engine()
    drop_db(engine)