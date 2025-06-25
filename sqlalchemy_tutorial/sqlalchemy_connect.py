from sqlalchemy import create_engine

db_url = "mysql+pymysql://root:spidy123@localhost/my_new_db"

engine = create_engine(db_url, echo=True)

try:
    connection = engine.connect()
    print("Connection to the database was successful!")
    connection.close()
except Exception as e:
    print(f"An error occurred while connecting to the database: {e}")   