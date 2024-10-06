from django.template.loader import render_to_string

from applications.core.agents import EmailAgent


def send_email_message(action, to_emails, context=None):
    if not context:
        context = {}

    if action == 'forgot-password':
        email_html_message = render_to_string('email/user_reset_password.html', context)
        agent = EmailAgent(
            to_emails=to_emails,
            subject='Reset your password',
            html_content=email_html_message,
        )
        agent.send_email()


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc) -> str:
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
