from constants.department import SUPERADMIN, COMMERCIAL, SUPPORT, MANAGEMENT
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.database_model import DatabaseModel
from constants.database import DB_URL


db = DatabaseModel(DB_URL)


def create_departments(self):
    """method to create base departments entries for creation of the superadmin account"""

    session = db.get_session()

    department_data = [
        {"name": COMMERCIAL, "description": "Service commercial"},
        {"name": SUPPORT, "description": "Service support"},
        {"name": MANAGEMENT, "description": "Service gestion"},
        {"name": SUPERADMIN, "description": "Service super administrateur"},
    ]

    for data in department_data:
        department = DepartmentModel()
        department.name = data["name"]
        department.description = data["description"]
        session.add(department)

    session.commit()
    session.close()


def create_super_admin(self):
    """method to create superadmin account"""

    session = db.get_session()

    employee_data = [
        {
            "username": SUPERADMIN,
            "department_id": 4,
            "email": "superadmin@epicevents.com",
            "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i",
        },
        {
            "username": SUPPORT,
            "department_id": 2,
            "email": "support@epicevents.com",
            "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i",
        },
        {
            "username": MANAGEMENT,
            "department_id": 3,
            "email": "management@epicevents.com",
            "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i",
        },
        {
            "username": COMMERCIAL,
            "department_id": 1,
            "email": "commercial@epicevents.com",
            "password": "$2y$10$IpoOpINijEvbie3PjdBzae/5SPTfoBnz7U27myUk3GBThO/fzGr2i",
        },
    ]

    for data in employee_data:
        employee = EmployeeModel()
        employee.username = data["username"]
        employee.password = data["password"]
        employee.email = data["email"]
        employee.department_id = (
            session.query(DepartmentModel).filter_by(name=data["username"]).first()
        ).id
        session.add(employee)

    session.commit()
    session.close()
