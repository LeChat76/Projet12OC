from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import IntegrityError
from constants.database import DB_URL
from views.utils_view import display_message
from models.employee_model import EmployeeModel
from constants.department import COMMERCIAL, SUPERADMIN
from models.database_model import Base
from models.database_model import DatabaseModel


class CustomerModel(Base):
    """ Customer class """

    def __init__(self, name, email, phone, company, employee_id):
        self.db = DatabaseModel(DB_URL)
        self.name = name
        self.email = email
        self.phone = phone
        self.company = company
        self.employee_id = employee_id
    
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    date_update = Column(TIMESTAMP, onupdate=text("CURRENT_TIMESTAMP"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
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
            display_message(f"Erreur lors de la modification du client : {str(e)}", True, True, 3)
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