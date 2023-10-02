from sentry_sdk import set_tag, capture_exception, capture_message


def send_to_sentry_NOK(tag1, tag2, exception):
    """ method to send report to Sentry when exception captured """
    
    set_tag(tag1, tag2)
    capture_exception(exception)

def send_creation_employee_message_to_sentry(loggedin_user, created_employee):
    """ method to send message to sentry """

    set_tag("employee", "creation")
    capture_message(f"L'utilisateur '{loggedin_user}' a créé l'employé '{created_employee}'.", level="info")

def send_update_employee_message_to_sentry(loggedin_user, created_employee):
    """ method to send message to sentry """

    set_tag("employee", "creation")
    capture_message(f"L'utilisateur '{loggedin_user}' a mis à jour l'employé '{created_employee}'.", level="info")

def send_contract_signature_message_to_sentry(loggedin_user, contract_id):
    """ method to send message to sentry """
    
    set_tag("contract", "signature")
    capture_message(f"L'utilisateur '{loggedin_user}' a signé le contrat numéro '{contract_id}'.", level="info")