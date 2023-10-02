from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, text, Float, Enum
from sqlalchemy.orm import relationship, joinedload
from models.database_model import Base
from constants.database import DB_URL
from utils.utils_view import display_message
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.database_model import DatabaseModel
from models.event_model import EventModel
from constants.department import MANAGEMENT, SUPERADMIN, COMMERCIAL
from utils.utils_sentry import send_to_sentry_NOK, send_contract_signature_message_to_sentry


class ContractModel(Base):
    """Contract class"""

    def __init__(self, price, due, status, customer, employee_id):
        self.db = DatabaseModel(DB_URL)
        self.price = price
        self.due = due
        self.status = status
        self.customer = customer
        self.employee_id = employee_id

    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False, default=0)
    due = Column(Float, nullable=False, default=0)
    date_creation = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    status = Column(Enum('SIGNED', 'NOT-SIGNED'), nullable=False, server_default="NOT-SIGNED")
    customer_id = Column(Integer, ForeignKey("customer.id", name="fk_contract_customer"), nullable=True)
    customer = relationship("CustomerModel", back_populates="contract", lazy="select")
    employee_id = Column(Integer, ForeignKey("employee.id", name="fk_contract_employee"), nullable=False)
    employee = relationship("EmployeeModel", back_populates="contract", lazy="select")
    event = relationship(
        "EventModel", uselist=False, back_populates="contract", lazy="select"
    )

    def __repr__(self):
        status_text = "Oui" if self.status == "SIGNED" else "Non"
        return f"Contrat numero '{self.id}' pour le client '{self.customer.name}' de la société '{self.customer.company}', signé : '{status_text}'."

    def __eq__(self, other):
        return self.id == other.id

    def add_contract(self, new_contract_obj):
        """
        method to add customer in the database
        INPUT : contract object
        RESULT : record of the new customer in the database
        """

        result = True

        try:
            session = self.db.get_session()
            session.add(new_contract_obj)
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("contract", "creation", e)
            result = None
        finally:
            session.close()
            return result

    def create_contract_object(self, choice):
        """
        method to create contract object from choice in list
        INPUT : str(choice in list)
        OUTPUT : contract object
        """

        contract_obj = None

        try:
            session = self.db.get_session()
            contract_obj = (
                session.query(ContractModel)
                .options(joinedload(ContractModel.customer))
                .offset(int(choice) - 1)
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "creation", e)
            display_message(
                f"Erreur lors de la creation de l'objet contrat: {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return contract_obj

    def create_contract_object_with_id(self, contract_id):
        """
        method to create contract object with contract ID
        INPUT : contract ID
        OUTPUT : contract object
        """

        contract_obj = None

        try:
            session = self.db.get_session()
            contract_obj = (
                session.query(ContractModel)
                .filter_by(id=contract_id)
                .options(joinedload(ContractModel.customer))
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "creation", e)
            display_message(
                f"Erreur lors de la creation de l'objet contrat: {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return contract_obj

    def create_contract_object_from_list(self, contract_choice_from_list, contract_obj_list):
        """
        method to create contract object with contract ID
        INPUT : contract chocie from list + contracts objects list
        OUTPUT : contract object
        """

        contract_obj = None
        contract_id = contract_obj_list[int(contract_choice_from_list) - 1].id

        try:
            session = self.db.get_session()
            contract_obj = (
                session.query(ContractModel)
                .filter_by(id=contract_id)
                .options(joinedload(ContractModel.customer))
                .first()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "creation", e)
            display_message(
                f"Erreur lors de la creation de l'objet contrat: {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return contract_obj

    def check_permission(self, employee_id):
        """
        function to check authorization to access to the contract menu
        INPUT : employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter_by(id=employee_id)
                .first()
            )
            if (
                employee_obj.department.name == MANAGEMENT
                or employee_obj.department.name == SUPERADMIN
            ):
                return True
            else:
                return False
        except Exception as e:
            send_to_sentry_NOK("contract", "permission", e)
            display_message(
                f"Erreur lors de la verification des permissions : {str(e)}",
                True,
                True,
                2,
            )
            return None
        finally:
            session.close()

    def check_permission_filter_menu(self, employee_id):
        """
        function to check authorization to access to the filter menu
        INPUT : employee id
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter_by(id=employee_id)
                .first()
            )
            if (
                employee_obj.department.name == COMMERCIAL
                or employee_obj.department.name == SUPERADMIN
            ):
                return True
            else:
                return False
        except Exception as e:
            send_to_sentry_NOK("contract", "permission", e)
            display_message(
                f"Erreur lors de la verification des permissions : {str(e)}",
                True,
                True,
                2,
            )
            return None
        finally:
            session.close()

    def check_permission_on_contract(self, employee_id, contract_obj):
        """
        function to check authorization to access to the contract for delete or update)
        INPUT : employee id + contract object
        OUTPUT : True of False
        """

        try:
            session = self.db.get_session()
            employee_obj = (
                session.query(EmployeeModel)
                .options(joinedload(EmployeeModel.department))
                .filter_by(id=employee_id)
                .first()
            )
            if (
                employee_obj.department.name == MANAGEMENT
                or employee_obj.department.name == SUPERADMIN
            ):
                return True
            if employee_obj.department.name == COMMERCIAL:
                customer_obj = (
                    session.query(CustomerModel)
                    .options(joinedload(CustomerModel.employee))
                    .filter_by(id=contract_obj.customer_id)
                    .first()
                )
                if customer_obj.employee_id == employee_obj.id:
                    return True
            else:
                return False
        except Exception as e:
            send_to_sentry_NOK("contract", "permission", e)
            display_message(
                f"Erreur lors de la verification des permissions : {str(e)}",
                True,
                True,
                2,
            )
            return None
        finally:
            session.close()

    def search_all_contracts(self):
        """method to select all contracts"""

        contracts_list = None

        try:
            session = self.db.get_session()
            contracts_list = (
                session.query(ContractModel)
                .options(joinedload(ContractModel.customer))
                .all()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "search", e)
            display_message(
                f"Erreur lors de la recherche des contrats : {str(e)}", True, True, 2
            )
        finally:
            session.close()
            return contracts_list

    def select_not_signed_contract(self):
        """
        method to select signed contracts
        OUPUT : list of non signed contracts
        """

        not_signed_contracts_list = None

        try:
            session = self.db.get_session()
            not_signed_contracts_list = (
                session.query(ContractModel)
                .options(joinedload(ContractModel.customer))
                .filter_by(status="NOT-SIGNED")
                .all()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "search", e)
            display_message(
                f"Erreur lors de la recherche des contrats nons signés : {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return not_signed_contracts_list

    def select_not_fully_payed_contracts(self):
        """
        method to select not fully payed contracts
        OUPUT : list of not fully payed contracts
        """

        not_fully_payed_contracts_list = None

        try:
            session = self.db.get_session()
            not_fully_payed_contracts_list = (
                session.query(ContractModel)
                .options(joinedload(ContractModel.customer))
                .filter(ContractModel.due != 0)
                .all()
            )
        except Exception as e:
            send_to_sentry_NOK("contract", "search", e)
            display_message(
                f"Erreur lors de la recherche des contrats nons totalement payés : {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return not_fully_payed_contracts_list

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

    def sign_contract(self, employee_id, contract_id):
        """
        method to sign contract
        INPUT : loggedin employee id + contract_obj
        RESULT : status field change to 'SIGNED'
        """

        try:
            session = self.db.get_session()
            employee_obj = session.query(EmployeeModel).get(employee_id)
            contract_obj = session.query(ContractModel).get(contract_id)
            contract_obj.status = "SIGNED"
            session.commit()
            send_contract_signature_message_to_sentry(employee_obj.username, contract_id)
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("contract", "update", e)
            display_message(
                f"Erreur lors de la signature du contrat : {str(e)}", True, True, 2
            )
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
            contract.price = contract_to_update_obj.price
            contract.due = contract_to_update_obj.due
            contract.status = contract_to_update_obj.status
            session.commit()
            display_message(
                f"Contrat '{contract_to_update_obj.id}' mis à jour avec succès!",
                True,
                True,
                2,
            )
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("contract", "update", e)
            display_message(
                f"Erreur lors de la modification du contrat : {str(e)}", True, True, 2
            )
            return None
        finally:
            session.close()

    def delete_contract(self, contract_id):
        """
        method to delete contract from database
        INPUT : contract id
        RESULT : deletion of the contract in the database
        """

        result = True

        try:
            session = self.db.get_session()
            contract_to_delete = (
                session.query(ContractModel).filter_by(id=contract_id).first()
            )
            session.delete(contract_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry_NOK("contract", "delete", e)
            result = None
        finally:
            session.close()
            return result

    def check_if_contract_exists(self, contract_id):
        """
        method to check if a contract exists
        INPUT = contract id
        OUPUT : True of False
        """

        result = True

        try:
            session = self.db.get_session()
            contract = session.get(ContractModel, contract_id)
            if not contract:
                result = False
        except Exception as e:
            send_to_sentry_NOK("contract", "search", e)
            display_message(
                f"Erreur lors de la recherche d'un contrat : {str(e)}", True, True, 2
            )
            result = None
        finally:
            session.close()
            return result

    def select_available_contracts(self, employee_id):
        """method to select all contracts not associated to an event AND signed"""

        filtered_contracts = None

        try:
            session = self.db.get_session()
            contracts_without_event = (
                session.query(ContractModel)
                .outerjoin(EventModel, ContractModel.id == EventModel.contract_id)
                .filter(EventModel.id.is_(None))
                .filter(ContractModel.status == "SIGNED")
            )
            filtered_contracts = [
                contract for contract in contracts_without_event
                if contract.customer is not None and contract.customer.employee_id == employee_id
            ]
        except Exception as e:
            send_to_sentry_NOK("contract", "search", e)
            display_message(
                f"Erreur lors de la selection des contrats sans evenements associés : {str(e)}",
                True,
                True,
                2,
            )
        finally:
            session.close()
            return filtered_contracts

    def check_if_contract_associated_to_employee(self, employee_id, contract_obj):
        """
        method to check if contract is associated to an customer associated to logged-in employee
        INPUT : employee ID + contract_obj
        OUPUT : True of False
        """

        customer = contract_obj.customer
        if customer.employee_id == employee_id:
            return True
        else:
            return False
