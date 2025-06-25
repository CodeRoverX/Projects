from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Database connection string
db_url = "mysql+pymysql://root:spidy123@localhost/my_new_db"
engine = create_engine(db_url, echo=False)

