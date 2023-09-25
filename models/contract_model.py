from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, text, Float
from sqlalchemy.orm import relationship, joinedload
from models.database_model import Base
from constants.database import DB_URL
from views.utils_view import display_message
from models.employee_model import EmployeeModel
from models.customer_model import CustomerModel
from models.database_model import DatabaseModel
from models.event_model import EventModel
from constants.department import MANAGEMENT, SUPERADMIN, COMMERCIAL
import sentry_sdk


class ContractModel(Base):
    """ Contract class """
    
    def __init__(self, customer_info, price, due, status, customer, employee_id):
        self.db = DatabaseModel(DB_URL)
        self.customer_info = customer_info
        self.price = price
        self.due = due
        self.status = status
        self.customer = customer
        self.employee_id = employee_id
    
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_info = Column(String(5000), nullable=True)
    price = Column(Float, nullable=False, default=0)
    due = Column(Float, nullable=False, default=0)
    date_creation = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    status = Column(String(10), nullable=False, server_default="NOT-SIGNED")
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    customer = relationship("CustomerModel", back_populates="contract", lazy="select")
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("EmployeeModel", back_populates="contract", lazy="select")
    event = relationship("EventModel", uselist=False, back_populates="contract", lazy="select")

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
            sentry_sdk.set_tag("contract", "creation")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de l'ajout du contrat : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def create_contract_object(self, choice):
        """
        method to create contract object with contract id
        INPUT : contract id
        OUTPUT : contract object
        """

        try:
            session = self.db.get_session()
            contract_obj = session.query(ContractModel).options(joinedload(ContractModel.customer)).offset(int(choice) - 1).first()
            return contract_obj
        except Exception as e:
            sentry_sdk.set_tag("contract", "creation")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la creation de l'objet contrat: {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission(self, employee_id):
        """
        function to check authorization to access to the contract menu
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
            sentry_sdk.set_tag("contract", "permission")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
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
            employee_obj = session.query(EmployeeModel).options(joinedload(EmployeeModel.department)).filter_by(id=employee_id).first()
            if employee_obj.department.name == COMMERCIAL or employee_obj.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            sentry_sdk.set_tag("contract", "permission")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
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
            sentry_sdk.set_tag("contract", "permission")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "search")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "search")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la recherche des contrats nons signés : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_not_fully_payed_contracts(self):
        """
        method to select not fully payed contracts
        OUPUT : list of not fully payed contracts
        """

        try:
            session = self.db.get_session()
            not_fully_payed_contracts_list = session.query(ContractModel).options(joinedload(ContractModel.customer)).filter(ContractModel.due != 0).all()
            return not_fully_payed_contracts_list
        except Exception as e:
            sentry_sdk.set_tag("contract", "search")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la recherche des contrats nons totalement payés : {str(e)}", True, True, 3)
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
            session.rollback()
            sentry_sdk.set_tag("contract", "update")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "update")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "delete")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "search")
            sentry_sdk.capture_exception(e)
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
            sentry_sdk.set_tag("contract", "search")
            sentry_sdk.capture_exception(e)
            display_message(f"Erreur lors de la selection des contrats sans evenements associés : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()
