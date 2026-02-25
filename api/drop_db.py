from engine import drop_db, initialize_engine

if __name__ == "__main__":
    print("Dropping database")
    engine = initialize_engine()
    drop_db(engine)