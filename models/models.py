from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, Enum, ForeignKey, text, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError
from constants.database_config import DB_URL
from views.utils_view import display_message
import bcrypt


Base = declarative_base()

class EventModel(Base):
    """ Event class """

    __tablename__ = 'event'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_contact = Column(String(255), nullable=False)
    date_start = Column(TIMESTAMP, nullable=False)
    date_end = Column(TIMESTAMP, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer(), nullable=False, default=0)
    notes = Column(String(1000), nullable=True)
    employee_id = Column(Integer(), ForeignKey('employee.id'), nullable=False)
    employee = relationship("EmployeeModel", back_populates="event")
    contract_id = Column(Integer(), ForeignKey('contract.id'), nullable=False)
    contract = relationship("ContractModel", uselist=False, back_populates="event")

class EmployeeModel(Base):

    def __init__(self):
        self.db = Database(DB_URL)

    __tablename__ = 'employee'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(String(7), nullable=False, server_default='ENABLE')
    department_id = Column(Integer(), ForeignKey('department.id'), nullable=False)
    department = relationship("DepartmentModel", back_populates="employee")
    customer = relationship("CustomerModel", back_populates="employee")
    contract = relationship("ContractModel", back_populates="employee")
    event = relationship("EventModel", back_populates="employee")

    def __repr__(self):
        return f"Employe '{self.username}', department '{self.department}'."
    
    def search_employee(self, input_username):
        """ method to search employee """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).filter_by(username=input_username).first()
            return employee
        except Exception as e:
            display_message(f"Erreur lors de la recherche employee : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
        
    def create_employee_object(self, employee_id):
        """
        method to select an customer in the database
        INPUT : employee id
        OUTPUT : employee object """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).filter_by(id=employee_id).first()
            return employee
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet employee : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()


    def check_password(self, input_password):
        """
        method to check password with the entered one
        INPUT : entered password
        OUTPUT : True if valid or False if invalid
        """

        db_password = self.password
        if bcrypt.checkpw(input_password.encode('utf-8'), db_password.encode('utf-8')):
            return True
        else:
            return None
    
    def check_permission_menu(self, department, employee_id):
        """
        check authorization of the employee to access to a specific menu
        INPUT : type of menu (customer, contract or event) and employee object
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if department == employee.department.name or employee.department.name == 'superadmin':
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission_customer(self, customer, employee_id):
        """
        function to check authorization of an employee on a customer
        (check if customer.employee_id == employee.id)
        INPUT : customer object + employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if customer.employee_id == employee.id or employee.department.name == 'superadmin':
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class DepartmentModel(Base):
    """ Department class """

    __tablename__ = 'department'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    employee = relationship("EmployeeModel", back_populates="department")

class CustomerModel(Base):
    """ Customer class """
    
    def __init__(self, name, email, phone, company, employee):
        self.db = Database(DB_URL)
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.employee = employee
    
    __tablename__ = 'customer'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    date_update = Column(TIMESTAMP, onupdate=text('CURRENT_TIMESTAMP'), nullable=True)
    employee_id = Column(Integer(), ForeignKey('employee.id'), nullable=False)
    employee = relationship("EmployeeModel", back_populates="customer")
    contract = relationship("ContractModel", back_populates="customer")

    def __repr__(self):
        return f'Client "{self.name}", email "{self.email}", telephone "{self.phone}" de la société "{self.company}".'

    def add_customer(self, new_customer):
        """
        method to add customer in the database
        INPUT : entered values for a new customer
        RESULT : record of the new customer in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_customer)
            session.commit()
            display_message("Client ajouté avec succès !", True, True, 2)
        except IntegrityError as e:
            session.rollback()
            display_message("Erreur lors de l'ajout du client : l'email est déjà associé à un autre client.", True, False, 0)
            display_message("Retour au menu....", False, False, 3)
            return None
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def search_all_customers(self):
        """ method to select all customers """

        try:
            session = self.db.get_session()
            customers_list = session.query(CustomerModel).all()
            return customers_list
        except Exception as e:
            display_message(f"Erreur lors de la recherche des clients : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def create_customer_object(self, choice):
        """
        method to select an customer in the database
        INPUT : choice (int or str) entered by employee
        OUTPUT : customer object """

        try:
            session = self.db.get_session()
            if isinstance(choice, str) and choice.isnumeric():
                customer = session.query(CustomerModel).offset(int(choice) - 1).first()
            else:
                customer = session.query(CustomerModel).filter_by(name = choice).first()
            return customer
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def update_customer(self, updated_customer):
        """
        method to update customer in database
        INPUT : customer object
        RESULT : update customer un database
        """

        try:
            session = self.db.get_session()
            customer = session.query(CustomerModel).filter_by(id=updated_customer.id).first()
            customer.name = updated_customer.name
            customer.email = updated_customer.email
            customer.phone = updated_customer.phone
            customer.company = updated_customer.company
            session.commit()
            display_message(f"Client '{updated_customer.name}' mis à jour avec succès!", True, True, 3)
        except Exception as e:
            display_message(f"Erreur lors de la modification du client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def delete_customer(self, customer):
        """
        method to delete customer from database
        INPUT : customer object
        RESULT : deletion of the customer in the database
        """

        try:
            session = self.db.get_session()
            customer_to_delete = session.query(CustomerModel).filter_by(id=customer.id).first()
            session.delete(customer_to_delete)
            session.commit()
            display_message(f"Client '{customer_to_delete.name}' supprimé avec succès!", True, True, 3)
        except Exception as e:
            display_message(f"Erreur lors de la suppresion du client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class ContractModel(Base):
    """ Contract class """
    
    def __init__(self, customer_info, price, due, status, customer, employee_id):
        self.db = Database(DB_URL)
        self.customer_info = customer_info
        self.price = price
        self.due = due
        self.status = status
        self.customer = customer
        self.employee_id = employee_id
    
    __tablename__ = 'contract'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_info = Column(String(5000), nullable=True)
    price = Column(Float(), nullable=False, default=0)
    due = Column(Float(), nullable=False, default=0)
    date_creation = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    status = Column(String(10), nullable=False, server_default='NOT-SIGNED')
    customer_id = Column(Integer(), ForeignKey('customer.id'), nullable=False)
    customer = relationship("CustomerModel", back_populates="contract")
    employee_id = Column(Integer(), ForeignKey('employee.id'), nullable=False)
    employee = relationship("EmployeeModel", back_populates="contract")
    event = relationship("EventModel", uselist=False, back_populates="contract")

    def __repr__(self):
        status_text = "OUI" if self.status == "SIGNED" else "NON"
        return f"Contrat numero '{self.id}' pour le client '{self.customer.name}' de la société '{self.customer.company}', signé : '{status_text}."

    def add_contract(self, new_contract):
        """
        method to add customer in the database
        INPUT : entered values for a new customer
        RESULT : record of the new customer in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_contract)
            session.commit()
            display_message(str(new_contract) + ' créé avec succes. Retour au menu...', True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def create_contract_object(self, contract_id):
        """
        method to create contract object
        INPUT : contract id
        OUTPUT : contract object """

        try:
            session = self.db.get_session()
            contract_obj = session.query(ContractModel).options(joinedload(ContractModel.customer)).filter_by(id=contract_id).first()
            return contract_obj
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet contrat: {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission_contract(self, employee_id):
        """
        function to check authorization of an employee on a customer
        (check if customer.employee_id == employee.id)
        INPUT : customer object & employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee_obj.department.name == "management" or employee_obj.department.name == 'superadmin':
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def search_all_contracts(self):
        """ method to select all contracts """

        try:
            session = self.db.get_session()
            contracts_list = session.query(ContractModel).options(joinedload(ContractModel.customer)).all()
            return contracts_list
        except Exception as e:
            display_message(f"Erreur lors de la recherche des contrats : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_signature(self, contract_obj):
        """
        check if contract is signed 
        INPUT : contract object
        OUTPUT : True or False
        """

        if contract_obj.status == "SIGNED":
            return True
        else:
            return False
    def update_contract(self, updated_contract):
        """
        method to update contract in database
        INPUT : contract object
        RESULT : update contract un database
        """

        try:
            session = self.db.get_session()
            contract = session.query(ContractModel).filter_by(id=updated_contract.id).first()
            contract.customer_info = updated_contract.customer_info
            contract.price = updated_contract.price
            contract.due = updated_contract.due
            contract.status = updated_contract.status
            session.commit()
            display_message(f"Contrat '{updated_contract.id}' mis à jour avec succès!", True, True, 3)
        except Exception as e:
            display_message(f"Erreur lors de la modification du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class Database:
    """ Database class """

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def tables_exist(self):
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        required_tables = ['customer', 'employee', 'contract', 'event']
        return all(table_name in table_names for table_name in required_tables)

    def get_session(self):
        return self.Session()
