from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, Enum, ForeignKey, text, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt


Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    department = Column(Enum('management', 'support', 'commercial', 'superadmin'), nullable=False)
    status = Column(String(7), nullable=False, server_default='ENABLE')
    customers = relationship("Customer", back_populates="employee")

    def __repr__(self):
        return f"Employe '{self.username}', department '{self.department}'."

class Customer(Base):
    def __init__(self, name, email, phone, company, employee_id):
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.employee_id = employee_id
    
    def __repr__(self):
        return f'Client "{self.name}", email "{self.email}", telephone "{self.phone}" de la société "{self.company}".'

    __tablename__ = 'customer'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    date_update = Column(TIMESTAMP, onupdate=text('CURRENT_TIMESTAMP'), nullable=True)
    employee_id = Column(Integer(), ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_contact = Column(String(255), nullable=False)
    date_start = Column(TIMESTAMP, nullable=False)
    date_end = Column(TIMESTAMP, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer(), nullable=False, default=0)
    notes = Column(String(1000), nullable=True)
    employee_id = Column(Integer(), ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee")

class Contract(Base):
    
    def __init__(self, customer_info, price, due, status, customer_id):
        self.customer_info = customer_info
        self.price = price
        self.due = due
        self.status = status
        self.customer_id = customer_id
    
    __tablename__ = 'contract'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_info = Column(String(5000), nullable=True)
    price = Column(Float(), nullable=False, default=0)
    due = Column(Float(), nullable=False, default=0)
    date_creation = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    status = Column(String(10), nullable=False, server_default='NOT-SIGNED')
    customer_id = Column(Integer(), ForeignKey('customer.id'), nullable=False)
    event_id = Column(Integer(), ForeignKey('event.id'), nullable=True)
    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event")

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        # self.user_id = None

    def create_tables(self):
        print('CREATE TABLE')
        Base.metadata.create_all(self.engine)

    def create_superadmin(self):
        session = self.get_session()
        superadmin = Employee(
            username='cedric',
            department='superadmin',
            password=bcrypt.hashpw('Toto1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        session.add(superadmin)
        session.commit()
        session.close()

    def tables_exist(self):
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        required_tables = ['customer', 'employee', 'contract', 'event']
        return all(table_name in table_names for table_name in required_tables)

    def get_session(self):
        return self.Session()