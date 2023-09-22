from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, text, create_engine, inspect, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError, DataError
from constants.database import DB_URL
from constants.department import MANAGEMENT, SUPPORT, SUPERADMIN, COMMERCIAL
from views.utils_view import display_message
import bcrypt


Base = declarative_base()

class EventModel(Base):
    """ Event class """

    def __init__(self):
        self.db = Database(DB_URL)

    __tablename__ = "event"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    date_start = Column(TIMESTAMP, nullable=False)
    date_end = Column(TIMESTAMP, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer(), nullable=False, default=0)
    notes = Column(String(1000), nullable=True)
    employee_id = Column(Integer(), ForeignKey("employee.id"), nullable=True)
    employee = relationship("EmployeeModel", back_populates="event")
    contract_id = Column(Integer(), ForeignKey("contract.id"), nullable=False)
    contract = relationship("ContractModel", uselist=False, back_populates="event")

    def __repr__(self):
        return f"Evenement '{self.id}' associé au contrat numero '{self.contract_id}'."

    def add_event(self, new_event):
        """
        method to add customer in the database
        INPUT : event object
        RESULT : record of the new event in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_event)
            session.commit()
            display_message("Evenement ajouté avec succès !", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def create_event_object(self, choice):
        """
        method to create an event object by offset
        INPUT : event choice from list
        OUTPUT : event object
        """

        try:
            session = self.db.get_session()
            event_obj = session.query(EventModel) \
                .options(joinedload(EventModel.employee)) \
                .options(joinedload(EventModel.contract)) \
                .offset(int(choice) - 1).first()
            return event_obj
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission_event(self, employee_id):
        """
        check authorization of the logged-in employee to access to the event creation menu
        INPUT : employee id
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee.department.name == COMMERCIAL or employee.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def check_permission_event_update(self, employee_id, event_obj):
        """
        check authorization of the logged-in employee to update an event
        INPUT : employee id + event object
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee.department.name == SUPERADMIN:
                return True
            elif employee.department.name == SUPPORT:
                if employee.id == event_obj.employee_id:
                    return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    
    def check_permission_event_assignation(self, employee_id):
        """
        check authorization of the logged-in employee to associate an event with an support employee
        INPUT : employee id
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee.department.name == MANAGEMENT or employee.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_unassigned_event(self):
        """ method to search unassigned events  """

        try:
            session = self.db.get_session()
            unassigned_event = session.query(EventModel) \
                .filter(EventModel.employee_id.is_(None)) \
                .all()
            return unassigned_event
        except Exception as e:
            display_message(f"Erreur lors de la recherche d'evenements non assignés : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def search_event(self, event_number):
        """
        method to search event
        INPUT : event ID entered by user
        OUPUT : event object or None
        """

        try:
            session = self.db.get_session()
            event = session.query(EventModel) \
                .options(joinedload(EventModel.employee)) \
                .options(joinedload(EventModel.contract)) \
                .filter_by(id=event_number).first()
            return event
        except Exception as e:
            display_message(f"Erreur lors de la recherche de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def assign_event(self, event_obj, employee_obj):
        """
        method to assign employee to an event
        INPUT : event_obj, employee obj
        RESULT : update event in the dataabse to fill field employee_id
        """

        try:
            session = self.db.get_session()
            event = session.query(EventModel).get(event_obj.id)
            event.employee_id = employee_obj.id
            session.commit()
            display_message(f"Evenement assigné à {employee_obj.username} avec succès...", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la mise à jour de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_all_events(self):
        """
        method to select all events
        OUTPUT : list of event object
        """

        try:
            session = self.db.get_session()
            event = session.query(EventModel).all()
            return event
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la recherche dans la table event : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def update_event(self, event_to_update):
        """
        method to update event in database
        INPUT : event object
        RESULT : update event un database
        """

        try:
            session = self.db.get_session()
            event = session.query(EventModel).get(event_to_update.id)
            event.date_start = event_to_update.date_start
            event.date_end = event_to_update.date_end
            event.location = event_to_update.location
            event.attendees = event_to_update.attendees
            event.notes = event_to_update.notes
            session.commit()
            display_message(f"Evenement '{event_to_update.id}' mis à jour avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la mise à jour de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def delete_event(self, event_obj):
        """
        method to delete event from database
        INPUT : event object
        RESULT : deletion of the event in the database
        """

        try:
            session = self.db.get_session()
            event_to_delete = session.query(EventModel).filter_by(id=event_obj.id).first()
            session.delete(event_to_delete)
            session.commit()
            display_message(f"Evenement numero '{event_to_delete.id}' supprimé avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la suppresion de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class EmployeeModel(Base):

    def __init__(self):
        self.db = Database(DB_URL)

    __tablename__ = "employee"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(String(7), nullable=False, server_default="ENABLE")
    department_id = Column(Integer(), ForeignKey("department.id"), nullable=False)
    department = relationship("DepartmentModel", back_populates="employee")
    customer = relationship("CustomerModel", back_populates="employee")
    contract = relationship("ContractModel", back_populates="employee")
    event = relationship("EventModel", back_populates="employee")

    def __repr__(self):
        return f"Employe '{self.username}', department '{self.department.name}'."
    
    def __eq__(self, other):
        if isinstance(other, EmployeeModel):
            return self.id == other.id
        return False

    def search_employee(self, input_username):
        """ method to search employee """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel) \
                .options(joinedload(EmployeeModel.department)) \
                .filter_by(username=input_username) \
                .first()
            return employee
        except Exception as e:
            display_message(f"Erreur lors de la recherche employee : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def select_support_employee(self):
        """ method to select support employees """

        try:
            session = self.db.get_session()
            support_employee = session.query(EmployeeModel) \
                .join(DepartmentModel) \
                .options(joinedload(EmployeeModel.department)) \
                .filter(or_(DepartmentModel.name == SUPPORT, DepartmentModel.name == SUPERADMIN)) \
                .all()
            return support_employee
        except Exception as e:
            display_message(f"Erreur lors de la recherche employee : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_all_employee(self):
        """ method to select support employees """

        try:
            session = self.db.get_session()
            support_employee = session.query(EmployeeModel) \
                .options(joinedload(EmployeeModel.department)) \
                .all()
            return support_employee
        except Exception as e:
            display_message(f"Erreur lors de la recherche d'employee : {str(e)}", True, True, 3)
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
        if bcrypt.checkpw(input_password.encode("utf-8"), db_password.encode("utf-8")):
            return True
        else:
            return None

    def create_employee_object(self, employee_id):
        """
        method to create employee object from employee ID
        INPUT : employee ID
        OUTPUT : employee object
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel) \
                .options(joinedload(EmployeeModel.contract)) \
                .options(joinedload(EmployeeModel.department)) \
                .filter_by(id=employee_id).first()
            return employee
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet employee : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def check_permission_employee(self, employee_id):
        """
        method to check if logged in user has permission to add employee
        INPUT : employee id of the logged in user
        OUTPUT : True of False 
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel) \
                .options(joinedload(EmployeeModel.department)) \
                .filter_by(id=employee_id).first()
            if employee.department.name == MANAGEMENT or employee.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la vérification du departement de l'utilisateur : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def add_employee(self, new_employee_obj):
        """
        method to add employee in the database
        INPUT : employee_obj
        RESULT : record of the new employee in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_employee_obj)
            session.commit()
            display_message("Employé ajouté avec succès !", True, True, 2)
        except IntegrityError as e:
            session.rollback()
            display_message("Erreur de la creation : nom d'utilisateur ou email deja utilisé.\nRetour au menu...", True, True, 3)
            return None
        except Exception as e:
            display_message(f"Erreur lors de la selection de l'employé : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def create_employee_object_from_list(self, choice):
        """
        method to create employee object from index
        INPUT : index of list entried by user from a list
        OUTPUT : employee object
        """

        try:
            session = self.db.get_session()
            employee_obj = session.query(EmployeeModel).offset(int(choice) - 1).first()
            return employee_obj
        except Exception as e:
            display_message(f"Erreur lors de la selection de l'employé : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def delete_employee(self, employee_obj):
        """
        method to delete employee from database
        INPUT : employee object
        RESULT : deletion of the employee in the database
        """

        try:
            session = self.db.get_session()
            employee_to_delete = session.query(EmployeeModel).filter_by(id=employee_obj.id).first()
            session.delete(employee_to_delete)
            session.commit()
            display_message(f"Employé '{employee_to_delete.username}' supprimé avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la suppresion de l'employé : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class DepartmentModel(Base):
    """ Department class """

    def __init__(self):
        self.db = Database(DB_URL)

    __tablename__ = "department"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    employee = relationship("EmployeeModel", back_populates="department")

    def __repr__(self):
        return f"Department '{self.name}', {self.description.lower()}."
    
    def select_all_department(self):
        """
        method to select all department
        OUPUT : department obj list
        """

        try:
            session = self.db.get_session()
            department_obj_list = session.query(DepartmentModel).all()
            return department_obj_list
        except Exception as e:
            display_message(f"Erreur lors de la selection des departements : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def create_department_object_from_list(self, choice):
        """
        method to create department object from index
        INPUT : index of list entried by user
        OUTPUT : department object
        """

        try:
            session = self.db.get_session()
            department_obj = session.query(DepartmentModel).offset(int(choice) - 1).first()
            return department_obj
        except Exception as e:
            display_message(f"Erreur lors de la selection du departement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class CustomerModel(Base):
    """ Customer class """
    
    def __init__(self, name, email, phone, company, employee_id):
        self.db = Database(DB_URL)
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.employee_id = employee_id
    
    __tablename__ = "customer"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    date_update = Column(TIMESTAMP, onupdate=text("CURRENT_TIMESTAMP"), nullable=True)
    employee_id = Column(Integer(), ForeignKey("employee.id"), nullable=False)
    employee = relationship("EmployeeModel", back_populates="customer")
    contract = relationship("ContractModel", back_populates="customer")

    def __repr__(self):
        return f"Client '{self.name}', email '{self.email}', telephone '{self.phone}' de la société '{self.company}'."

    def check_permission_customer(self, employee_id, customer_obj):
        """
        function to check authorization of an logged-in employee to modify a customer
        (check if employee.department.name department is 'superadmin' or 'management')
        INPUT : employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee.department.name == SUPERADMIN:
                return True
            elif employee.department.name == COMMERCIAL:
                if customer_obj.employee_id == employee_id:
                    return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission_customer_menu(self, employee_id):
        """
        check authorization of the logged-in employee to access to the creation/deletion menu
        INPUT : employee id
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee.department.name == COMMERCIAL or employee.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()


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
        method to create customer object from index (list)
        INPUT : choice (int or str) entered by employee
        OUTPUT : customer object
        """

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
    
    def create_customer_object_with_id(self, customer_id):
        """
        method to create customer object ID
        INPUT : ID of the customer
        OUTPUT : customer object
        """

        try:
            session = self.db.get_session()
            customer = session.query(CustomerModel).get(customer_id)
            return customer
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()


    def update_customer(self, customer_to_update):
        """
        method to update customer in database
        INPUT : customers object
        RESULT : update customer un database
        """

        try:
            session = self.db.get_session()
            customer = session.query(CustomerModel).get(customer_to_update.id)
            customer.name = customer_to_update.name
            customer.email = customer_to_update.email
            customer.phone = customer_to_update.phone
            customer.company = customer_to_update.company
            customer.employee_id = customer_to_update.employee_id
            session.commit()
            display_message(f"Client '{customer_to_update.name}' mis à jour avec succès!", True, True, 3)
        except IntegrityError as e:
            session.rollback()
            display_message("Erreur lors de la modification du client : l'email est déjà associé à un autre client.", True, False, 0)
            display_message("Retour au menu....", False, False, 3)
            return None
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def delete_customer(self, customer_obj):
        """
        method to delete customer from database
        INPUT : customer object
        RESULT : deletion of the customer in the database
        """

        try:
            session = self.db.get_session()
            customer_to_delete = session.query(CustomerModel).filter_by(id=customer_obj.id).first()
            session.delete(customer_to_delete)
            session.commit()
            display_message(f"Client '{customer_to_delete.name}' supprimé avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
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
    
    __tablename__ = "contract"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    customer_info = Column(String(5000), nullable=True)
    price = Column(Float(), nullable=False, default=0)
    due = Column(Float(), nullable=False, default=0)
    date_creation = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    status = Column(String(10), nullable=False, server_default="NOT-SIGNED")
    customer_id = Column(Integer(), ForeignKey("customer.id"), nullable=False)
    customer = relationship("CustomerModel", back_populates="contract")
    employee_id = Column(Integer(), ForeignKey("employee.id"), nullable=False)
    employee = relationship("EmployeeModel", back_populates="contract")
    event = relationship("EventModel", uselist=False, back_populates="contract")

    def __repr__(self):
        status_text = "Oui" if self.status == "SIGNED" else "Non"
        return f"Contrat numero '{self.id}' pour le client '{self.customer.name}' de la société '{self.customer.company}', signé : '{status_text}'."

    def add_contract(self, new_contract_obj):
        """
        method to add customer in the database
        INPUT : contract object
        RESULT : record of the new customer in the database
        """
        
        try:
            session = self.db.get_session()
            session.add(new_contract_obj)
            session.commit()
            display_message(str(new_contract_obj) + " créé avec succes. Retour au menu...", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def create_contract_object(self, choice):
        """
        method to create contract object with contract id
        INPUT : contract id
        OUTPUT : contract object """

        try:
            session = self.db.get_session()
            contract_obj = session.query(ContractModel).options(joinedload(ContractModel.customer)).offset(int(choice) - 1).first()
            return contract_obj
        except Exception as e:
            display_message(f"Erreur lors de la creation de l'objet contrat: {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission(self, employee_id):
        """
        function to check authorization to access to the contract menu (dept management or superadmin authorized only)
        INPUT : employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee_obj.department.name == MANAGEMENT or employee_obj.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def check_permission_on_contract(self, employee_id, contract_obj):
        """
        function to check authorization to access to the contract (for delete or update). Only customer owner + commercial employee can do.
        INPUT : employee id + contract object
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = session.query(EmployeeModel) \
                .options(joinedload(EmployeeModel.department)) \
                .filter_by(id=employee_id).first()
            if employee_obj.department.name == MANAGEMENT or employee_obj.department.name == SUPERADMIN:
                return True
            if employee_obj.department.name == COMMERCIAL:
                customer_obj = session.query(CustomerModel) \
                .options(joinedload(CustomerModel.employee)) \
                .filter_by(id=contract_obj.customer_id).first()
                if customer_obj.employee_id == employee_obj.id:
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

    def select_not_signed_contract(self):
        """
        method to select signed contracts
        OUPUT : list of non signed contracts
        """

        try:
            session = self.db.get_session()
            not_signed_contracts_list = session.query(ContractModel).options(joinedload(ContractModel.customer)).filter_by(status="NOT-SIGNED").all()
            return not_signed_contracts_list
        except Exception as e:
            display_message(f"Erreur lors de la recherche des contrats nons signés : {str(e)}", True, True, 3)
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

    def sign_contract(self, contract_obj):
        """
        method to sign contract
        INPUT : contract_obj
        RESULT : status field change to 'SIGNED'
        """

        try:
            session = self.db.get_session()
            contract = session.query(ContractModel).get(contract_obj.id)
            contract.status = "SIGNED"
            session.commit()
        except Exception as e:
            display_message(f"Erreur lors de la signature du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def update_contract(self, contract_to_update_obj):
        """
        method to update contract in database
        INPUT : contract object
        RESULT : update contract un database
        """

        try:
            session = self.db.get_session()
            contract = session.query(ContractModel).get(contract_to_update_obj.id)
            contract.customer_info = contract_to_update_obj.customer_info
            contract.price = contract_to_update_obj.price
            contract.due = contract_to_update_obj.due
            contract.status = contract_to_update_obj.status
            session.commit()
            display_message(f"Contrat '{contract_to_update_obj.id}' mis à jour avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la modification du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def delete_contract(self, contract_obj):
        """
        method to delete contract from database
        INPUT : contract obj
        RESULT : deletion of the contract in the database
        """

        try:
            session = self.db.get_session()
            contract_to_delete = session.query(ContractModel).filter_by(id=contract_obj.id).first()
            session.delete(contract_to_delete)
            session.commit()
            display_message(f"Contrat némro '{contract_to_delete.id}' supprimé avec succès!", True, True, 3)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la suppresion du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
    
    def check_if_contract_exists(self, contract_id):
        """
        method to check if a contract exists
        INPUT = contract id
        OUPUT : True of False
        """
        try:
            session = self.db.get_session()
            contract = session.query(ContractModel).filter_by(id=contract_id).first()
            if contract:
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de la recherche d'un contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_available_contracts(self):
        """ method to select all contracts not associated to an event AND signed """

        try:
            session = self.db.get_session()
            contracts_without_event = session.query(ContractModel) \
                .outerjoin(EventModel, ContractModel.id == EventModel.contract_id) \
                .options(joinedload(ContractModel.customer)) \
                .filter(EventModel.id.is_(None)) \
                .filter(ContractModel.status=="SIGNED") \
                .all()
            return contracts_without_event
        except Exception as e:
            display_message(f"Erreur lors de la selection des contrats sans evenements associés : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

class Database:
    """ Database class """

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """ method to create tables + superadmin account """
        Base.metadata.create_all(self.engine)
        self.create_departments_entries()
        self.create_super_admin()
    
    def create_departments_entries(self):
        """ method to create base departments entries for creation of the superadmin account """

        session = self.get_session()    

        department_data = [
            {"name": COMMERCIAL, "description": "Service commercial"},
            {"name": SUPPORT, "description": "Service support"},
            {"name": MANAGEMENT, "description": "Service gestion"},
            {"name": SUPERADMIN, "description": "Service super administrateur"}
        ]

        for data in department_data:
            department = DepartmentModel()
            department.name = data["name"]
            department.description = data["description"]
            session.add(department)

        session.commit()
        session.close()


    def create_super_admin(self):
        """ method to create superadmin account """

        session = self.get_session()

        employee_data = [
            {"username": SUPERADMIN, "department_id": 4, "email": "superadmin@epicevents.com", "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i"},
            {"username": SUPPORT, "department_id": 2, "email": "support@epicevents.com", "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i"},
            {"username": MANAGEMENT, "department_id": 3, "email": "management@epicevents.com", "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i"},
            {"username": COMMERCIAL, "department_id": 1, "email": "commercial@epicevents.com", "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i"},
        ]

        for data in employee_data:
            employee = EmployeeModel()
            employee.username = data["username"]
            employee.password = data["password"]
            employee.email = data["email"]
            employee.department_id = (session.query(DepartmentModel).filter_by(name=data["username"]).first()).id
            session.add(employee)

        session.commit()
        session.close()

    def tables_exist(self):
        """ method to check if tables already exists """

        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        required_tables = ["customer", "employee", "contract", "event"]
        return all(table_name in table_names for table_name in required_tables)

    def get_session(self):
        return self.Session()
