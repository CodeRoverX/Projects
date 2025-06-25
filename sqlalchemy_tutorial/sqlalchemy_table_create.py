from sqlalchemy import create_engine, MetaData, Integer, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker

# db connection string
db_url = "mysql+pymysql://root:spidy123@localhost/my_new_db"
engine = create_engine(db_url, echo=False)

try:
    connection = engine.connect()
    print("Connection to the database was successful!")
    connection.close()
except Exception as e:
    print(f"An error occurred while connecting to the database: {e}")   

    
#create a basse class
base = declarative_base()

#define a table
class User(base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    email = Column(String(20))
    
    
#create the table
base.metadata.create_all(engine)    

## Create a session
Session  = sessionmaker(bind=engine)
session = Session()

#insert a new user
# new_user1 = User(name='Elon', email='elon@123')
# new_user2 = User(name='Musk', email='musk@123')
# session.add(new_user1)
# session.add(new_user2)
# session.commit()

# # Insert more users
# more_users = [
#     User(name='Alice', email='alice@example.com'),
#     User(name='Bob', email='bob@example.com'),
#     User(name='Charlie', email='charlie@example.com'),
#     User(name='Diana', email='diana@example.com'),
#     User(name='Eve', email='eve@example.com')
# ]

# session.add_all(more_users)
# session.commit()

#update a user
user_to_update1 = session.query(User).filter_by(name='Elon').first()
user_to_update2 = session.query(User).filter_by(name='Musk').first()
if user_to_update1:
    user_to_update1.email = 'new_elon@example.com'
    session.commit()
if user_to_update2:
    user_to_update2.email = 'new_musk@example.com'
    session.commit()
    
    
#delete a user
user_to_delete = session.query(User).filter_by(id=7).first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()


# Query the user
results = session.query(User).all()
for user in results:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")