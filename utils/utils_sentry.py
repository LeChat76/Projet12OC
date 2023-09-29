from sentry_sdk import add_breadcrumb, set_tag, capture_exception


def send_to_sentry_NOK(tag1, tag2, exception):
    """ method to send report to Sentry when exception captured """
    
    set_tag(tag1, tag2)
    capture_exception(exception)

def send_to_sentry_OK(category, message, level):
    """ method to send breadcrumb to Sentry when no exception captured """
    
    add_breadcrumb(category=category, message=message, level=level)