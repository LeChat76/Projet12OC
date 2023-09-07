from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, Enum, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    role = Column(Enum('management', 'support', 'commercial'), nullable=False)
    status = Column(String(7), nullable=False, server_default='ENABLE')
    customers = relationship("Customer", back_populates="employee")

    def __repr__(self):
        return f'Employe {self.username}, role {self.role}.'

class Customer(Base):
    def __init__(self, name, email, phone, company, employee_id):
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.employee_id = employee_id

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

    def __repr__(self):
        return f'Client {self.name} de la societe {self.company}.'

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
