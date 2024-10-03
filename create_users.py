
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, UserRole
from werkzeug.security import generate_password_hash

# Add the repository directory to the system path
sys.path.append('earth-616')

# Connect to the SQLite database
def create_admin_user():
    engine = create_engine('sqlite:///earth-616/facilities.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generate a hashed password for admin
    admin_password = 'admin'
    hashed_admin_password = generate_password_hash(admin_password)

    # Create a new admin user
    new_admin = User(username='admin_user', hashed_password=hashed_admin_password, role=UserRole.admin)

    # Add the new admin user to the session and commit
    session.add(new_admin)
    session.commit()

    # Verify the admin user was added
    admin_user = session.query(User).filter_by(username='admin_user').first()
    print('Admin user added:', admin_user.username, admin_user.role)

    # Close the session
    session.close()


def create_student_user():
    engine = create_engine('sqlite:///earth-616/facilities.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generate a hashed password for student
    student_password = 'student_user'
    hashed_student_password = generate_password_hash(student_password)

    # Create a new student user
    new_student = User(username='student_user', hashed_password=hashed_student_password, role=UserRole.student)

    # Add the new student user to the session and commit
    session.add(new_student)
    session.commit()

    # Verify the student user was added
    student_user = session.query(User).filter_by(username='student_user').first()
    print('Student user added:', student_user.username, student_user.role)

    # Close the session
    session.close()

if __name__ == '__main__':
    create_admin_user()
    create_student_user()
