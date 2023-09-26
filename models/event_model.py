from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from models.database_model import Base
from utils.utils_view import display_message
from constants.database import DB_URL
from constants.department import COMMERCIAL, SUPERADMIN, SUPPORT, MANAGEMENT
from models.employee_model import EmployeeModel
from models.database_model import DatabaseModel
from utils.utils_sentry import send_to_sentry


class EventModel(Base):
    """ Event class """

    def __init__(self):
        self.db = DatabaseModel(DB_URL)

    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_start = Column(TIMESTAMP, nullable=False)
    date_end = Column(TIMESTAMP, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False, default=0)
    notes = Column(String(1000), nullable=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=True)
    employee = relationship("EmployeeModel", back_populates="event")
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    contract = relationship("ContractModel", uselist=False, back_populates="event")

    def __repr__(self):
        return f"Evenement '{self.id}' associé au contrat numero '{self.contract_id}'."

    def add_event(self, new_event):
        """
        method to add event in the database
        INPUT : event object
        RESULT : record of the new event in the database
        """
        
        result = True

        try:
            session = self.db.get_session()
            session.add(new_event)
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry("event", "creation", e)
            result = None
        finally:
            session.close()
            return result

    def create_event_object(self, choice):
        """
        method to create an event object by offset
        INPUT : event choice from list
        OUTPUT : event object
        """

        event_obj = None

        try:
            session = self.db.get_session()
            event_obj = session.query(EventModel) \
                .options(joinedload(EventModel.employee)) \
                .options(joinedload(EventModel.contract)) \
                .offset(int(choice) - 1).first()
        except Exception as e:
            send_to_sentry("event", "creation", e)
            display_message(f"Erreur lors de la creation de l'objet evenement : {str(e)}", True, True, 3)
        finally:
            session.close()
            return event_obj

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
            send_to_sentry("event", "permission", e)
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def check_permission_menu_filter_event(self, employee_id):
        """
        check authorization of the logged-in employee to access to the event filter menu
        INPUT : employee id
        OUPUT : True or False
        """

        try:
            session = self.db.get_session()
            employee = session.query(EmployeeModel).filter_by(id=employee_id).first()
            if employee.department.name == SUPPORT or employee.department.name == SUPERADMIN:
                return True
            else:
                return False
        except Exception as e:
            send_to_sentry("event", "permission", e)
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
            send_to_sentry("event", "permission", e)
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
            send_to_sentry("event", "permission", e)
            display_message(f"Erreur lors de la verification des permissions : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_unassigned_event(self):
        """ method to search unassigned events  """

        unassigned_event = None

        try:
            session = self.db.get_session()
            unassigned_event = session.query(EventModel) \
                .filter(EventModel.employee_id.is_(None)) \
                .all()
        except Exception as e:
            send_to_sentry("event", "search", e)
            display_message(f"Erreur lors de la recherche d'evenements non assignés : {str(e)}", True, True, 3)
        finally:
            session.close()
            return unassigned_event

    def select_in_progress_event(self):
        """ method to select events where date has not passed """

        unassigned_event = None

        try:
            session = self.db.get_session()
            unassigned_event = session.query(EventModel) \
                .filter(EventModel.date_end > datetime.now()) \
                .all()
        except Exception as e:
            send_to_sentry("event", "search", e)
            display_message(f"Erreur lors de la recherche d'evenements non terminés : {str(e)}", True, True, 3)
        finally:
            session.close()
            return unassigned_event

    def search_event(self, event_number):
        """
        method to search event
        INPUT : event ID entered by user
        OUPUT : event object or None
        """

        event = None

        try:
            session = self.db.get_session()
            event = session.query(EventModel) \
                .options(joinedload(EventModel.employee)) \
                .options(joinedload(EventModel.contract)) \
                .filter_by(id=event_number).first()
        except Exception as e:
            send_to_sentry("event", "search", e)
            display_message(f"Erreur lors de la recherche de l'evenement : {str(e)}", True, True, 3)
        finally:
            session.close()
            return event

    def assign_event(self, event_obj, employee_obj):
        """
        method to assign employee to an event
        INPUT : event_obj, employee obj
        RESULT : update event in the database to fill field employee_id
        """

        try:
            session = self.db.get_session()
            event = session.query(EventModel).get(event_obj.id)
            event.employee_id = employee_obj.id
            session.commit()
            display_message(f"Evenement assigné à {employee_obj.username} avec succès...", True, True, 3)
        except Exception as e:
            session.rollback()
            send_to_sentry("event", "update", e)
            display_message(f"Erreur lors de l'assignation de l'evenement : {str(e)}", True, True, 3)
            return None
        finally:
            session.close()

    def select_all_events(self):
        """
        method to select all events
        OUTPUT : list of event object
        """

        event = None

        try:
            session = self.db.get_session()
            event = session.query(EventModel).all()
        except Exception as e:
            send_to_sentry("event", "search", e)
            display_message(f"Erreur lors de la recherche dans la table event : {str(e)}", True, True, 3)
        finally:
            session.close()
            return event

    def select_assigned_events(self, employee_id):
        """
        method to select events assigned to the logged-in employee
        INPUT : employee id
        OUPUT : events object list
        """

        event = None

        try:
            session = self.db.get_session()
            event = session.query(EventModel) \
                .filter(EventModel.employee_id == employee_id) \
                .all()
        except Exception as e:
            send_to_sentry("event", "search", e)
            display_message(f"Erreur lors de la recherche des evenements assignés : {str(e)}", True, True, 3)
        finally:
            session.close()
            return event

    def update_event(self, event_to_update_obj):
        """
        method to update an event in database
        INPUT : event object
        RESULT : update event un database
        """

        result = True

        try:
            session = self.db.get_session()
            event = session.get(EventModel, event_to_update_obj.id)
            event.date_start = event_to_update_obj.date_start
            event.date_end = event_to_update_obj.date_end
            event.location = event_to_update_obj.location
            event.attendees = event_to_update_obj.attendees
            event.notes = event_to_update_obj.notes
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry("event", "update", e)
            result = None
        finally:
            session.close()
            return result

    def delete_event(self, event_id):
        """
        method to delete an event from database
        INPUT : event id
        RESULT : deletion of the event in the database
        """

        result = True

        try:
            session = self.db.get_session()
            event_to_delete = session.get(EventModel, event_id)
            session.delete(event_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            send_to_sentry("event", "delete", e)
            result = None
        finally:
            session.close()
            return result