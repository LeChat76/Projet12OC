from sqlalchemy import Column, String, Integer, ForeignKey, or_, Enum
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import IntegrityError
from utils.utils_view import display_message
from constants.department import SUPPORT, SUPERADMIN, MANAGEMENT
from constants.database import DB_URL
from models.department_model import DepartmentModel
from models.database_model import Base
from models.database_model import DatabaseModel
import bcrypt, os
from utils.utils_sentry import send_to_sentry_NOK, send_creation_employee_message_to_sentry


class EmployeeModel(Base):
    """Employee class"""

    def __init__(self):
        self.db = DatabaseModel(DB_URL)

    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(Enum('ENABLE', 'DISABLE'), nullable=False, server_default="ENABLE")
    token = Column(String(512), nullable=True)
    department_id = Column(Integer, ForeignKey("department.id", name="fk_employee_department"), nullable=False)
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
        """
        method to search employee
        INPUT : user name intried
        OUPUT : employee obj or None
        """

        employee = None

        try:
            session = self.db.get_session()
            employee = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter_by(username=input_username)
                .filter(EmployeeModel.status == "ENABLE")
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("employee", "search", e)
            display_message(
                f"Erreur lors de la recherche employee : {str(e)}", True, True, 2
            )
        finally:
            session.close()
            return employee

    def select_support_employee(self):
        """method to select support employees"""

        support_employees = None

        try:
            session = self.db.get_session()
            support_employees = (
                session.query(EmployeeModel)
                .join(DepartmentModel)
                .options(joinedload(EmployeeModel.department))
                .filter(DepartmentModel.name == SUPPORT, EmployeeModel.status == "ENABLE")
                .all()
            )
        except Exception as e:
            send_to_sentry_NOK("employee", "search", e)
            display_message(
                f"Erreur lors de la recherche d'employés : {str(e)}", True, True, 2
            )
        finally:
            session.close()
            return support_employees

    def select_all_employee(self):
        """method to select all employees"""

        employees = None

        try:
            session = self.db.get_session()
            employees = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter(EmployeeModel.status == "ENABLE")
                .all()
            )
        except Exception as e:
            send_to_sentry_NOK("employee", "search", e)
            display_message(
                f"Erreur lors de la recherche d'employés : {str(e)}", True, True, 2
            )
        finally:
            session.close()
            return employees

    def check_password(self, account_password, input_password):
        """
        method to check password with the entered one
        INPUT : entered password
        OUTPUT : True if valid or False if invalid
        """

        if bcrypt.checkpw(
            input_password.encode("utf-8"), account_password.encode("utf-8")
        ):
            return True
        else:
            return None

    def create_employee_object(self, employee_id):
        """
        method to create employee object from employee ID
        INPUT : employee ID
        OUTPUT : employee object
        """

        employee = None

        try:
            session = self.db.get_session()
            employee = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.contract))
                .options(joinedload(EmployeeModel.department))
                .filter_by(id=employee_id)
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("employee", "creation", e)
            display_message(
                f"Erreur lors de la creation de l'objet employee : {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return employee

    def check_permission_employee(self, employee_id):
        """
        method to check if logged-in user has permission to add employee
        INPUT : employee id of the logged-in employee
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter_by(id=employee_id)
                .first()
            )
            if (
                employee.department.name == MANAGEMENT
                or employee.department.name == SUPERADMIN
            ):
                return True
            else:
                return False
        except Exception as e:
            send_to_sentry_NOK("employee", "permission", e)
            display_message(
                f"Erreur lors de la vérification du departement de l'utilisateur : {str(e)}",
                True,
                True,
                2,
            )
            return None
        finally:
            session.close()

    def add_employee(self, employee_id, new_employee_obj):
        """
        method to add employee in the database
        INPUT : loggedin employee id + employee_obj
        RESULT : record of the new employee in the database
        """

        result = True

        try:
            session = self.db.get_session()
            employee_obj = session.get(EmployeeModel, employee_id)
            session.add(new_employee_obj)
            session.commit()
            send_creation_employee_message_to_sentry(employee_obj.username, new_employee_obj.username)
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("employee", "creation", e)
            result = None
        finally:
            session.close()
            return result

    def create_employee_object_from_list(self, choice):
        """
        method to create employee object from index
        INPUT : index of list entried by user from a list
        OUTPUT : employee object
        """

        employee_obj = None

        try:
            session = self.db.get_session()
            employee_obj = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter(EmployeeModel.status != 'DISABLE')
                .offset(int(choice) - 1)
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("employee", "creation", e)
            display_message(
                f"Erreur lors de la selection de l'employé : {str(e)}", True, True, 2
            )
        finally:
            session.close()
            return employee_obj

    def delete_employee(self, employee_id):
        """
        method to delete employee from database
        INPUT : employee object
        RESULT : deletion of the employee in the database
        """

        result = True

        try:
            session = self.db.get_session()
            employee_to_delete = session.get(EmployeeModel, employee_id)
            employee_to_delete.status = "DISABLE"
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("employee", "delete", e)
            result = None
        finally:
            session.close()
            return result

    def update_employee(self, employee_to_update):
        """
        method to update employee in database
        INPUT : employee object
        RESULT : update employee un database
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).get(employee_to_update.id)
            employee.username = employee_to_update.username
            employee.password = employee_to_update.password
            employee.email = employee_to_update.email
            employee.department_id = employee_to_update.department_id
            employee.status = employee_to_update.status
            session.commit()
            display_message(
                f"Client '{employee_to_update.username}' mis à jour avec succès!",
                True,
                True,
                2,
            )
        except IntegrityError as e:
            session.rollback()
            send_to_sentry_NOK("employee", "update", e)
            display_message(
                "Erreur lors de la modification de l'employee : l'email est déjà associé à un autre employee.",
                True,
                False,
                0,
            )
            display_message("Retour au menu....", False, False, 2)
            return None
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("employee", "update", e)
            display_message(
                f"Erreur lors de la modification de l'employee : {str(e)}",
                True,
                True,
                2,
            )
            return None
        finally:
            session.close()

    def delete_last_employee(self):
        """ method to delete last employee from database """

        result = True

        try:
            session = self.db.get_session()
            employee_to_delete = session.query(EmployeeModel).order_by(EmployeeModel.id.desc()).first()
            session.delete(employee_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("employee", "delete", e)
            result = None
        finally:
            session.close()
            return result
    
    def store_token_in_database(self, token, employee_id):
        """
        method to store generatred token in employee in database
        INPUT : token + employee_id
        RESULT : token recorded to the database
        """

        result = True

        try:
            session = self.db.get_session()
            employee_obj = session.get(EmployeeModel, employee_id)
            employee_obj.token = token
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("employee", "record_token", e)
            result = False
        finally:
            session.close()
            return result
    
    def store_token_in_file(self, token):
        """ method to store toke in token.txt in root folder """

        result = True

        try:
            # script_path = os.path.abspath(__file__)
            # root_folder = os.path.dirname(script_path)
            with open("token.tkn", "w") as fichier:
                fichier.write(token)
        except Exception as e:
            send_to_sentry_NOK("token", "record_in_file", e)
            result = False
        finally:
            return result
    
    def read_token(self):
        """
        method to read token stored in file
        OUPUT = token
        """

        token = None

        try:
            with open("token.tkn", 'r') as fichier:
                token = fichier.read()
        except Exception as e:
            send_to_sentry_NOK("token", "read_file", e)
        finally:
            return token
    
    def create_employee_obj_ty_token(self, token):
        """
        method to create employee object with token
        INPUT : token
        OUPUT : employee object or None if invalid token
        """

        employee_obj = None

        try:
            session = self.db.get_session()
            employee_obj = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter(EmployeeModel.token == token)
                .first()
            )
            return employee_obj
        except Exception as e:
            send_to_sentry_NOK("employee", "create_employee_object_with_token", e)
        finally:
            return employee_obj
