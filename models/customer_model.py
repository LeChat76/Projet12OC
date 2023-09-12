from models.models import Customer
from models.models import Database
from constants.database_config import DB_URL
from views.utils_view import display_message


class CustomerModel:
    """ Customer class """

    def __init__(self):
        self.db = Database(DB_URL)

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
            display_message("Client ajouté avec succès !", True, 2)
        except Exception as e:
            session.rollback()
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True,2 )
            return None
        finally:
            session.close()
    
    def search_customer(self, employee):
        """ method to select customers associated to an employee """

        try:
            session = self.db.get_session()
            customers_list = session.query(Customer).all()
            return customers_list
        except Exception as e:
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True, 2)
            return None
        finally:
            session.close()
    
    def create_customer_object(self, choice):
        """
        method to select an customer in the database
        INPUT : choice (int or str) entered by employee
        OUTPUT : customer object """

        try:
            session = self.db.get_session()
            if isinstance(choice, str) and choice.isnumeric():
                customer = session.query(Customer).offset(int(choice) - 1).first()
            else:
                customer = session.query(Customer).filter_by(name = choice).first()
            return customer
        except Exception as e:
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True, 2)
            return None
        finally:
            session.close()
    
    def update_customer(self, updated_customer):
        """
        method to update customer in database
        INPUT : customer object
        RESULT : update customer un database
        """

        try:
            session = self.db.get_session()
            customer = session.query(Customer).filter_by(id=updated_customer.id).first()
            customer.name = updated_customer.name
            customer.email = updated_customer.email
            customer.phone = updated_customer.phone
            customer.company = updated_customer.company
            session.commit()
            display_message(f"Client '{updated_customer.name}' mis à jour avec succès!", True, 2)
        except Exception as e:
            display_message(f"Erreur lors de l'ajout du client : {str(e)}", True, 2)
            return None
        finally:
            session.close()

    def delete_customer(self, customer):
        """
        method to delete customer from database
        INPUT : customer object
        RESULT : deletion of the customer in the database
        """

        try:
            session = self.db.get_session()
            customer_to_delete = session.query(Customer).filter_by(id=customer.id).first()
            session.delete(customer_to_delete)
            session.commit()
            display_message(f"Client '{customer_to_delete.name}' supprimé avec succès!", True, 2)
        except Exception as e:
            display_message(f"Erreur lors de la suppresion du client : {str(e)}", True, 2)
            return None
        finally:
            session.close()

