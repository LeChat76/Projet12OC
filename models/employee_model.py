from models.models import Database, Employee
from constants.constants import DB_URL
import bcrypt


class EmployeeModel():
    """ Employee class """

    def __init__(self):
        self.db = Database(DB_URL)
    
    def search_employee(self, input_username):
        """ 
        method to search employee
        INPUT : entered username
        OUTPUT : employee object
        """

        session = self.db.get_session()
        employee = session.query(Employee).filter_by(username=input_username).first()
        if employee:
            return employee
        else:
            return None
    
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

