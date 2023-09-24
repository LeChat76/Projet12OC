from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from views.utils_view import display_message
from models.database_model import DatabaseModel
from constants.database import DB_URL
from models.database_model import Base


class DepartmentModel(Base):
    """ Department class """

    def __init__(self):
        self.db = DatabaseModel(DB_URL)

    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
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