from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table 
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload

db_url = "mysql+pymysql://root:spidy123@localhost/my_new_db"
engine = create_engine(db_url, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

student_course = Table(
    'student_course',Base.metadata,
    Column('student_id',Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True), 
)


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # Many-to-many relationship
    courses = relationship('Course', secondary='student_course', back_populates='students')
    
class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    
    # Many-to-many relationship
    students = relationship('Student', secondary='student_course', back_populates='courses')
    
Base.metadata.create_all(engine)


#inserting

# stud1 = Student(name="Uguh")
# stud2 = Student(name="Alice")

# course1 = Course(title='Python')
# course2 = Course(title='SQL')
# course3 = Course(title='Data Science')

# session.add_all([stud1, stud2, course1, course2, course3])
# session.commit()

# print("Students and courses added successfully!")

# Fetch students and courses from DB
# uguh = session.query(Student).filter_by(name="Uguh").first()
# alice = session.query(Student).filter_by(name="Alice").first()

# python = session.query(Course).filter_by(title="Python").first()
# sql = session.query(Course).filter_by(title="SQL").first()
# ds = session.query(Course).filter_by(title="Data Science").first()

# uguh.courses.append(python)
# uguh.courses.append(sql)

# alice.courses.append(python)
# alice.courses.append(ds)

# session.commit()

# print("Courses assigned to students successfully!")

#Update : Change course title from "SQL" to "Advanced SQL"

# course_to_update = session.query(Course).filter_by(title='sql').first()
# if course_to_update:
#     course_to_update.title = 'Advanced SQL'
#     session.commit()
#     print("Course title updated successfully!")
# else:
#     print("Course not found!")

#✅ Step 5: Remove Alice from Python Course

# alice = session.query(Student).filter_by(name="Alice").first()

# if alice:
#     py_course = session.query(Course).filter_by(title="Python").first()
#     if py_course in alice.courses:
#         alice.courses.remove(py_course)
#         session.commit()
#         print(f"Alice has been removed from the {py_course.title} course.")
#     else:
#         print("Alice is not enrolled in the Python course.")
# else:
#     print("Alice not found in the database.")


#✅ 1. Query: Courses for Uguh

# uguh = session.query(Student).filter_by(name="Uguh").first()

# if uguh:
#     print(f"Courses for {uguh.name}")
#     for course in uguh.courses:
#         print(f"- {course.title}")
# else:
#     print("Uguh not found in the database.")

##✅ 2. Query: Students in Python Course

# py_cou = session.query(Course).filter_by(title="Python").first()

# if py_cou:
#     print(f'Students enrolled in {py_cou.title} course:')
#     for stud in py_cou.students:
#         print(f"- {stud.name}")
# else:
#     print("Python course not found in the database.")
# # Close the session
# session.close()
# # Close the session
# # session.close()
# # Close the engine
# # engine.dispose()


# uguh = session.query(Student).filter_by(name="Uguh").first()
# ds = session.query(Course).filter_by(title="Data Science").first()

# if uguh and ds:
#     uguh.courses.append(ds)
#     session.commit()
#     print(f"{uguh.name} has been enrolled in the {ds.title} course.")
# else:
#     print("Either Uguh or Data Science course not found in the database.")


# Default (optional, it's the default)
# courses = relationship("Course", secondary=student_course, back_populates="students", lazy='subquery')
# uguh = session.query(Student).filter_by(name="Uguh").first()
# print("Step 1: Lazy (select)")
# for course in uguh.courses:
#     print(course.title)


# stud = session.query(Student).options(joinedload(Student.courses)).all()
# for s in stud:
#     print(f"Stud:{s.name}")
#     for c in s.courses:
#         print(f"  Course: {c.title}")


# ✅ Context Manager Pattern (Preferred)

# from sqlalchemy.orm import Session as SessionType

# with SessionType(bind=engine) as session:
#     student = Student(name="Uguh")
#     session.add(student)
#     session.commit()