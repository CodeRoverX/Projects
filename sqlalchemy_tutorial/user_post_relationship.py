from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Create an engine
db_url = "mysql+pymysql://root:spidy123@localhost/my_new_db"
engine = create_engine(db_url, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define User table / Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    email = Column(String(30))
    
    # 1 user has many posts# Define relationship to Post
    posts = relationship("Post", back_populates="user")
    
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Each post belongs to one user
    user = relationship("User",back_populates="posts")
    
Base.metadata.create_all(engine)


#Insert a User and Their Posts

user1 = User(name="Uguh", email="uguh@example.com")

post1 = Post(title="My First Post", content="This is the content of my first post.", user=user1)
post2 = Post(title="My Second Post", content="This is the content of my second post.", user=user1)

session.add(user1)
session.commit()

#Query: Access Posts from User
user = session.query(User).filter_by(name="Uguh").first()

print(f"\n📌 Posts by {user.name}:")
for post in user.posts:
    print(f"- {post.title}: {post.content}")
    
#Query a post and get the author
post = session.query(Post).filter_by(title="My First Post").first()
print(f"\n📝 '{post.title}' was written by {post.user.name}")