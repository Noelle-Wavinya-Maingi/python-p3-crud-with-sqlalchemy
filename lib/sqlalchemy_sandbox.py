#!/usr/bin/env python3

# Import necessary modules
from datetime import datetime
from sqlalchemy import (
    create_engine,
    desc,
    func,
    Index,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a declarative base
Base = declarative_base()

# Define the Student class
class Student(Base):
    # Define the table name
    __tablename__ = "students"

    # Create an index on the 'name' column
    Index("index_name", "name")

    # Define columns for the table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # Define a custom representation for the class
    def __repr__(self):
        return f"Student {self.id}: " + f"{self.name}, " + f"Grade {self.grade}"

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Create an in-memory SQLite database engine
    engine = create_engine("sqlite:///:memory:")

    # Create the tables defined by the classes that inherit from Base
    Base.metadata.create_all(engine)

    # Create a session maker bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create instances of the Student class
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(year=1987, month=3, day=14),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(year=1912, month=6, day=23),
    )

    # Bulk insert the student instances and commit changes
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # Query students using various queries
    students = session.query(Student).all()
    names = session.query(Student.name).all()
    students_by_name = session.query(Student.name).order_by(Student.name).all()
    students_by_grade = (
        session.query(Student.name, Student.grade).order_by(desc(Student.grade)).all()
    )
    oldest_student = (
        session.query(Student.name, Student.birthday).order_by(Student.birthday).first()
    )
    student_count = session.query(func.count(Student.id)).first()
    query = (
        session.query(Student)
        .filter(Student.name.like("%Alan%"), Student.grade == 11)
        .all()
    )

    # Delete a record from the database
    del_query = session.query(Student).filter(Student.name == "Albert Einstein")
    del_query.delete()

    # Print query results
    print([student for student in students])
    print(names)
    print(students_by_name)
    print(students_by_grade)
    print(oldest_student)
    print(student_count)
    for record in query:
        print(record.name)

    # Update student grades
    session.query(Student).update({Student.grade: Student.grade + 1})

    # Print updated records
    print([(student.name, student.grade) for student in session.query(Student)])
    print(albert_einstein)
