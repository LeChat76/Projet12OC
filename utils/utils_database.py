from constants.department import SUPERADMIN, COMMERCIAL, SUPPORT, MANAGEMENT
from models.department_model import DepartmentModel
from models.employee_model import EmployeeModel
from models.database_model import DatabaseModel
from models.customer_model import CustomerModel
from models.contract_model import ContractModel
from models.event_model import EventModel
from constants.database import DB_URL
from utils.utils_sentry import send_to_sentry_NOK


db = DatabaseModel(DB_URL)


def create_departments():
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


def create_super_admin():
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

def create_employees():
    """ method to create employees for the demonstration """

    session = db.get_session()

    customer_data = [
        {"name": "Kevin3", "email": "kevin3@kevin.fr", "phone": "0665565656", "company": "Kev Comp", "employee_id": 1},
        {"name": "AZERTY", "email": "d.d@m.fr", "phone": "0506551245", "company": "Azert or Not?", "employee_id": 1},
        {"name": "Kevin2", "email": "d@d.fr", "phone": "0325544568", "company": "Flipper Zero G'", "employee_id": 1},
        {"name": "Tilt", "email": "a@a.com", "phone": "+331 25 65 98 74", "company": "Flipp and Go", "employee_id": 1},
        {"name": "www", "email": "w@w.fr", "phone": "0800 033 022", "company": "wWw & Web", "employee_id": 1},
        {"name": "Kevin", "email": "kevin@kevin.com", "phone": "0661994560", "company": "Kev Comp", "employee_id": 4},
        {"name": "Rasta", "email": "09@gmail.com", "phone": "666-777-888", "company": "R&K Company", "employee_id": 1},
        {"name": "Yo!", "email": "5@g.fr", "phone": "01 23 45 78 89", "company": "Wesh Studio", "employee_id": 1},
        {"name": "Cedrik", "email": "d@f.fr", "phone": "07 77 66 65 52", "company": "Ced K", "employee_id": 4},
        {"name": "LG", "email": "g@g.fr", "phone": "02 01 02 01 06", "company": "Lady G", "employee_id": 1},
        {"name": "GKSD", "email": "0@fr.fr", "phone": "06 60 06 60 06", "company": "GKSD Corporation", "employee_id": 1},
        {"name": "AZERTY2", "email": "d@fr.com", "phone": "+33 2 32 94 04 56", "company": "AZERTY or Not", "employee_id": 1},
        {"name": "Kevin Casey", "email": "kevin@startup.io", "phone": "+678 123 456 78", "company": "Cool Startup LLC", "employee_id": 1},
        {"name": "Titi", "email": "titi@titi.fr", "phone": "666-666-666", "company": "Titi & Gros Minet Corp", "employee_id": 4}
    ]

    try:
        for data in customer_data:
            customer = CustomerModel(None, None, None, None, None)
            customer.name = data["name"]
            customer.email = data["email"]
            customer.phone = data["phone"]
            customer.company = data["company"]
            customer.employee_id = data["employee_id"]
            
            session.add(customer)
        
        session.commit()
    except Exception as e:
        session.rollback()
        send_to_sentry_NOK("database", "employees_creation", e)
    finally:
        session.close()

def create_contracts():
    """ method to create contracts for the demonstration """

    session = db.get_session()

    contract_data = [
        {"id": 1000000, "price": 1500.0, "due": 1000.0, "status": "NOT-SIGNED", "customer_email": "kevin@kevin.com", "employee_id": 3},
        {"id": 1000001, "price": 2500.0, "due": 0.0, "status": "SIGNED", "customer_email": "d@f.fr", "employee_id": 3},
        {"id": 1000002, "price": 4000.0, "due": 0.0, "status": "SIGNED", "customer_email": "09@gmail.com", "employee_id": 3},
        {"id": 1000003, "price": 1500.0, "due": 0.0, "status": "SIGNED", "customer_email": "kevin@kevin.com", "employee_id": 3},
        {"id": 1000004, "price": 2500.0, "due": 0.0, "status": "NOT-SIGNED", "customer_email": "d@f.fr", "employee_id": 3},
        {"id": 1000005, "price": 4000.0, "due": 3500.0, "status": "NOT-SIGNED", "customer_email": "09@gmail.com", "employee_id": 3},
    ]

    try:
        for data in contract_data:
            contract = ContractModel(None, None, None, None, None)
            contract.id = data["id"]
            contract.price = data["price"]
            contract.due = data["due"]
            contract.status = data["status"]
            customer_obj = (
                session.query(CustomerModel)
                .filter_by(email = data["customer_email"])
                .first()
            )
            contract.customer_id = customer_obj.id
            contract.employee_id = data["employee_id"]

            session.add(contract)
        session.commit()
    except Exception as e:
        session.rollback()
        send_to_sentry_NOK("database", "contracts_creation", e)
    finally:
        session.close()

    contracts_obj_list = session.query(ContractModel).all()

    customers_ids = [6,9,7,6,9,7]

    counter = 0

    for contract_obj in contracts_obj_list:
        contract_obj.customer_id = customers_ids[counter]
        session.commit()
        counter += 1
    
    session.close()

def create_events():
    """ method to create events for the demonstration """

    session = db.get_session()

    event_data = [
        {"id": 1000000, "date_start": "2024-07-16 12:00:00", "date_end": "2024-07-16 20:00:00", "location": "97 allée des Platanes, 76520 Boos", "attendees": 30, "notes": "Anniversaire du bézo!", "employee_id": 2, "contract_id": 1000003},
        {"id": 1000001, "date_start": "2023-06-24 13:00:00", "date_end": "2023-06-25 14:00:00", "location": "Marie de Paris, 75000, Paris", "attendees": 5000, "notes": "Grand marathon de Noël à Paris!", "employee_id": None, "contract_id": 1000002},
        {"id": 1000002, "date_start": "2023-06-04 13:00:00", "date_end": "2023-06-05 14:00:00", "location": "Rue de Rouen, 76000, Rouen", "attendees": 75, "notes": "Elections pestilentielles", "employee_id": 2, "contract_id": 1000001},
        {"id": 1000003, "date_start": "2023-09-28 10:00:00", "date_end": "2023-09-28 16:30:00", "location": "rue de Rouen, 76000, Rouen", "attendees": 20, "notes": "Forum créateurs d'entreprise", "employee_id": None, "contract_id": 1000000}
    ]
    try:
        for data in event_data:
            event = EventModel()
            event.id = data["id"]
            event.date_start = data["date_start"]
            event.date_end = data["date_end"]
            event.location = data["location"]
            event.attendees = data["attendees"]
            event.notes = data["notes"]
            event.contract_id = data["contract_id"]

            session.add(event)

        session.commit()

        employee_id = (
            session.query(EmployeeModel)
            .filter_by(email = "support@epicevents.com")
            .first()
        ).id
        event_obj_1000000 = session.get(EventModel, 1000000)
        event_obj_1000000.employee_id = employee_id
        event_obj_1000002 = session.get(EventModel, 1000002)
        event_obj_1000002.employee_id = employee_id

        session.commit()

    except Exception as e:
        session.rollback()
        send_to_sentry_NOK("database", "events_creation", e)
    finally:
        session.close()
  

