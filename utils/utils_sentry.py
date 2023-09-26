import sentry_sdk

def send_to_sentry(tag1, tag2, exception):
    """ method to send report to Sentry """
    
    sentry_sdk.set_tag(tag1, tag2)
    sentry_sdk.capture_exception(exception)